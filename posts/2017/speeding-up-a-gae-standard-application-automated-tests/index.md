---
title: "Speeding up a GAE-standard application automated tests"
date: "2017-05-29"
tags: 
  - "development"
  - "python"
  - "test"
---

 

If you’re developing on a Google AppEngine standard environment, you know how slow the dev\_appserver is. You have surely experienced its long setup times on the first request being served (probably because of the SQLite based datastore implementation). And also the long shutdown times (when the search indexes are being written to the disk).

[LumApps](https://www.lumapps.com/en/) had an automated tests suite, split up in scenarii. Each scenario was performing a set of requests to a (new) dev\_appserver instance. The isolation was made restoring the datastore and search index before playing a scenario. A specific scenario was in charge of recreating the reference datastore and search index. To complete the isolation, the instance was rebooted between two scenarii.

In this situation, the scenarii took 46’ to complete. We didn’t have an idea of how much code was being covered. We just evaluated the number of public endpoints being called (this gave a gross evaluation). Debugging the server in order to get more information about what was going on was also kind of prehistoric.

And last, on my system the tests took even more than 46’. Much more. And I was unable to test my code impacts.

## The journey begins

At first, I started coding unit tests. Since I was new to Python and GAE, that allowed me to discover coverage.py, pytest, mock, and the GAE testbed. I was delighted about their maturity level and the functionalities they sported out. In particular, thanks Ned, thanks Alex.

After a few weeks writing unit tests, my thoughts went back to the existing automated tests. I knew that I could make something to speed them up. How do they work? They’re LumRest scenarii (LumRest is an [open-source project](https://github.com/lumapps/lumRest)). You just put in a [yaml file](https://github.com/lumapps/lumRest/blob/master/scenarios/urlshortener.yaml) a list of commands, where each command corresponds to an endpoint that shall be called. Each command has a body (in the form of: a json file, inline json, a list of fields and the corresponding values). When in the scope of a command, you have a few keywords that allow you to eval python code or jsonpath expressions, just before or just after emitting the request. You can save a response, in order to reuse it. And you can check that the response corresponds to a certain model/statuscode.

## Discovering endpoints and messages

The first step I took was to discover endpoints and messages. When addressing google-endpoints, you have to provide a typed request and you will receive a typed response. Type validation takes place when querying endpoints. Discovering endpoints was pretty easy, using the `get_api_classes()` method.

```
our_endpoints = endpoints.api(name='application',
 version='v1',
 description="Application APIs",
 documentation="http://api.company.com/application/",
 allowed_client_ids=CLIENT_IDS)

def get_endpoints_map(endpoints_def):
 api_classes = endpoints_def.get_api_classes()
 paths = {}
 for cls in api_classes:
 base_path = cls.api_info._ApiInfo__path
 for _, method_desc in cls._ServiceClass__remote_methods.items():
 method_key = '{}/{}'.format(base_path, method_desc.method_info._MethodInfo__path)
 paths[method_key] = (cls, method_desc)
 assert paths
 return paths

api_map = get_endpoints_map(our_endpoints)
# > api_map
{'user/list': <function>}
{'user/get': <function>}
[..]
```

This function hasn’t evolved at all, that’s a sign that it was good enough to get its job done. The discovery doesn’t take long, and it is being executed only once, at the beginning of the tests.

## Call the endpoints…

Once the endpoints were known, how to use them? I had the function to call, and that means also the request/response types. But our implementation was just passing json objects and getting back json objects.

On the one way side, I have searched the google code for the classes transforming a json request in a Message, but after a while I decided that implementing a simple recursive algorithm would have taken less time. I was probably wrong, because I kept modifying this function until the last days. But with about 50 lines of code, today everything seems to work.

```
def process_value(value_type, value, is_repeated, contextualize=None):
 current = value
 variant = value_type.variant
 if is_repeated and not isinstance(value, list):
 current = [value]
 if is_repeated and value is None:
 current = []
 if variant == Variant.ENUM:
 current = value_type.type(value)
 if variant == Variant.STRING and isinstance(value, int):
 current = unicode(value)
 if variant == Variant.INT32 and isinstance(value, basestring):
 current = int(value)
 if variant == Variant.MESSAGE:
 if is_repeated:
 current = []
 if isinstance(value, list):
 current.extend(process_value(value_type, item, False, contextualize) for item in value)
 elif isinstance(value, dict):
 list_elem = value_type.type()
 for key, item in value.items():
 if hasattr(list_elem, key):
 current = [process_value(
 getattr(value_type.type, key), item, value_type.type.repeated, contextualize
 )]
 else:
 raise ValueError('unexpected type {} for value'.format(type(value)))
 else:
 current = value_type.type()
 for key, item in value.items():
 if hasattr(current, key):
 subtype = getattr(value_type.type, key)
 setattr(current, key, process_value(subtype, item, subtype.repeated, contextualize))
 else:
 context = contextualize() if contextualize else ''
 logger.warning("%s the request type <%s> lacks a '%s' attribute", context, value_type, key)
 return current

def call_endpoint(target_class, method_desc, contextualize=None, **kwargs):
 request_type = method_desc.remote.request_type
 response_type = method_desc.remote.response_type
 request = request_type()
 if kwargs:
 for key, value in kwargs.items():
 if hasattr(request, key):
 value_type = getattr(request_type, key, None)
 if value_type:
 setattr(request, key, process_value(value_type, value, value_type.repeated, contextualize))
 else:
 setattr(request, key, value)
 else:
 context = contextualize() if contextualize else ''
 logger.warning("%s the request type <%s> lacks a '%s' attribute", context, request_type, key)

instance = target_class()
 if isinstance(instance, Service):
 instance.initialize_request_state(FakeHttpRequestState())

response = method_desc(instance, request)
 assert isinstance(response, response_type)
 return response
```

## .. and get something back

Then it came the time of serializing the response. In this case, I was so dissatisfied with my implementation, that after a few days I searched more in depth the google code, finding at last ProtoJson. This is probably not the code used by the appserver (because the serialization sometimes differs, when it’s question of nested empty dictionaries/lists).

```
def typed_response_to_dict(instance):
 converted = instance
 if isinstance(instance, Message):
 original_instance = copy.deepcopy(instance)
 converted = json.loads(ProtoJson().encode_message(instance))
 # fixette: to pass the workflow tests (dictionaries which contain only None values are dropped) till the root
 # this is not true for the dev_appserver
 original_properties = getattr(original_instance, 'properties', {})
 properties = getattr(instance, 'properties', {})
 if original_properties and not properties:
 converted['properties'] = {}
 elif isinstance(instance, BaseEndpointsModel):
 logger.warning('We are receiving a BaseEndpointsModel instead of a protorpc.messages.Message')
 converted = instance.to_dict_full()
 return converted
```

## Stubbing out the dev\_appserver — a rapid introduction

The pitch of this dissertation was about the slugginess of the dev\_appserver. So, how to make it faster? When you’re unit-testing a GAE application, you can use the [testbed](https://cloud.google.com/appengine/docs/standard/python/tools/localunittesting). It’s a great piece of code. My knowledge of the dev\_appserver is small, yet, but.. It uses a set of stubs to fullfill its tasks. On the production nvironment, these stubs are being replaced with real services, queried through an api\_proxy. On the local environment, the dev\_appserver uses Sqlite as datastore stub, the RAM for the memcache and the search\_index stubs. In the unit tests context, you will be using an alternative DatastoreStub (based on simple pickling/unpickling of objects to the filesystem) and the same stubs for the search\_index and memcache. You could be willing to use also the urlfetch stub (when consuming data from google cloud storage, for example). It’s good to know that you will have to initialize the blobstore stub along with the urlfetch stub:

```
self.testbed.init_blobstore_stub()
self.testbed.init_urlfetch_stub()
```

And, if your application is made up of several modules, you will also need the modules stub. I suggest you to read the topic on [http://stackoverflow.com/a/28228867](http://stackoverflow.com/a/28228867), in order to know how to initialize all the modules required by your application. And, at last, if your application uses deferred tasks and/or background tasks, you will have to initialize the taskqueue stub specifying the path to the folder containing the `queues.yaml` file. I have not mentioned the email stub or the appidentity stub (or all the other stubs you could need for your tests). It’s better to read the official documentation, there’s always a useful option you could make profit of.

### Persist data

If you like to persist the data at the end of a test, you can use the datastore\_file=path, save\_changes=True option of the init\_datastore\_stub. For the search index stub, you will have to get the stub and use its Write method. We use this technique for our ‘generator’ scenario.

#### At the test setup

```
self.testbed = testbed.Testbed()
self.testbed.activate()
self.testbed.init_memcache_stub()
self.testbed.init_datastore_v3_stub(datastore_file=self.DATASTORE_FILE, save_changes=True)
[..]
from google.appengine.ext.testbed import SEARCH_SERVICE_NAME
if not enable:
 self.testbed._disable_stub(SEARCH_SERVICE_NAME)
 return
from google.appengine.api.search import simple_search_stub
if simple_search_stub is None:
 from google.appengine.ext.testbed import StubNotSupportedError
 raise StubNotSupportedError('Could not initialize search API')
stub = simple_search_stub.SearchServiceStub(index_file=self.SEARCH_INDEX_FILE)
self.testbed._register_stub(SEARCH_SERVICE_NAME, stub)
```

#### At the test teardown

```
# nothing to do with the datastore stub (thanks to the save_changes kwarg)
self.search_stub.Write()
```

## LumRest grammar support

Since the topic of this document is about performances, I won’t give you details. In order to execute the existing tests, I have had to support the DSL they were written in. It has taken a certain time, and it’s not fully supported, yet. The commands supported today allow my layer to execute 99% of the tests (and to get hints about what’s going wrong or what could be improved)

## Background tasks execution

The testbed doesn’t provide any kind of task runner. It’s up to you to decide whether to execute the tasks that have been queued during the unit test (or just check they’re there). The official google documentation gives you an example about how to execute deferred tasks. But old applications probably use task handlers. A task handler is registered as a special route, at your application startup. At last, a task will just be a method of the http request handler. And in order to interact with a task, you will have to provide a specially crafted HTTP Request. I have already spoken about reimplementing the serialization/deserialization of requests and responses.. But this time it has been definitely simpler. In facts, I kept some bugs in the execution logic till the last days just to spice up my experience :-) The whole taskrunner logic takes about 80 lines of code, and will be the longest except in this dissertation.

```
class AggregateException(Exception):
 def __init__(self, message, errors):
 super(AggregateException, self).__init__(message)
 self.errors = errors

class FakeHttpRequestState(object):
 def __init__(self, **kwargs):
 self.headers = kwargs

class FakeSessionStore(object):
 def __init__(self):
 self.config = {'cookie_args': {}}

def get_session(self, factory=None):
 return factory('mock', self).get_session()

def get_secure_cookie(self, *args, **kwargs):
 return ''

class TaskRunner(object):
 def __init__(self):
 self.routes_patterns = []
 for route in routes: # your web application routes
 pattern = re.compile(route[0])
 self.routes_patterns.append((pattern, route[1]))

@staticmethod
 def __init_handler(handler, task):
 environ = {}
 method = task.method.upper()
 url = task.url
 if task.payload:
 args = {method: task.payload}
 else:
 args = {}

handler.request = Request.blank(url, environ=environ, headers=task.headers, **args)
 handler.session_store = FakeSessionStore()

def run_task(self, task):
 if task.url == '/_ah/queue/deferred':
 deferred.run(task.payload)
 else:
 for route in self.routes_patterns:
 if route[0].match(task.url):
 handler_cls = route[1]
 break
 if not handler_cls:
 raise ValueError("handler not found for task: %s/%", task.url, task.payload)
 handler = handler_cls()
 self.__init_handler(handler, task)
 method = getattr(handler, task.method.lower())
 method()

def safe_run_task(self, task):
 try:
 self.run_task(task)
 except Exception as err:
 task_desc = task.url
 if task.url == '/_ah/queue/deferred':
 import pickle
 task_unpickled = pickle.loads(task.payload)
 task_desc = task_unpickled[1][:2]
 if len(task_desc) == 2:
 task_desc = u'{}.{}'.format(type(task_desc[0]).__name__, task_desc[1])
 else:
 task_desc = repr(task_unpickled[0].func_code)
 logger.exception("caught exception during the execution of the task '%s': %s", task_desc, err)
 return err

def run_tasks(self, tasks):
 exceptions = []
 for task in tasks:
 val = self.safe_run_task(task)
 if val:
 exceptions.append(val)
 if exceptions:
 raise AggregateException(
 'caught one or more exceptions during the execution of background tasks', exceptions
 )
```

## Stubbing out the HTTP communications

The application was still interacting with third party APIs. This was a pain in the neck, because of sluggy/unstable network connections (yeah, they still exist in 2017). For this reason, at some point we started using [vcrpy](https://vcrpy.readthedocs.io/en/latest/index.html). This kind of tool replaces all the classes/methods responsible of communicating with a remote server via HTTP. The replacements record all the exchanges (on their first execution). And if a scenario has already been registered, vcrpy uses the recorded exchanges to simulate the dialog between our application and the third party server. This way of proceeding is safe unless the third party APIs undergo a breaking change. For our tests, that meant decorating all the methods with the attribute:

```
@vcr.use_cassette(cassette_library_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/cassettes'))
```

## Conclusion

### What’s strange, today

- The GAE DatastoreFileStub seems to have some bugs related to concurrency. One of our tests was failing since the results were not consistent. Mocking the `threading.Thread()``start` and `join` methods allowed us to pass past these buggy behaviors.
- The sortOrder doesn’t seem to work for datetimes (when querying objects from the datastore — ndb, and sorting them by their createdAt date, we get results that are not sorted).

### Results met

- The tests execute faster. They take only 20% of the time they took initially.
- We are able to get branch-level code coverage indicators. We know which portions of the code can be changed confidently.
- We are able to debug a test using pdb (or pydev).
- I a able to evaluate confidently what I’m breaking! And it doesn’t take an entire night ;-)

### What could be improved

- drop the support for the LumRest grammar and write the tests directly in python. To accomplish this aim, we shall be able to execute the tests on the stubs AND on the dev\_appserver (like lumrest did). This could allow us to detect misbehaviors in the google appengine communication layers. The best way to do this kind of tests, would be to use a dedicated deployed test environment (identical to the production one). Advantage of this solution: you don’t need to learn lumRest to write a test.
- surely, the current lumrest-stubs implementation could be made yet faster.

 

TL;DR

​
