JMDE -- JSON Metadata Discovery Engine
===============================

JMDE is the outcome of my undergraduate thesis work. It takes an arbitrary JSON
document and attempts to classify it within the DBpedia ontology, effectively
providing metadata for an input document. This metadata comes in the form of a
JSON-LD `@type` annotation, which points to an ontology entry.

Todo
----
This software isn't currently in working order. There's a lot of refactoring
and restructuring to be done before it can be usable. Most of the code was
written quickly, to accommodate a narrow research timeline. Getting it out of
prototype form will require the following (at least):

* Serious refactoring of the "backend" (retrieve.py),
* Development of a convenient surface API,
* Refactoring and simplification of the `treeclassifier.py` module.

Why?
----
This was borne from experimental research, so don't ask me for *too* much
concrete real-world application. However, ontology metadata is very important
for linked data applications, and the popularity of JSON warrants the creation
of more tools that support this kind of metadata.

The primary concern is this: how do you know what to do with a JSON document
once you have it? Most of the time, your client application needs to be tightly
coupled to the format of the document. This works for a majority of the current
use-cases of JSON -- the structure of the document (i.e. the meaning of the
data contained therein) is implicit in the client program and not in the
document itself.

However, it doesn't allow for software that is capable of handling *arbitrary*
JSON documents, where there isn't the possibility of the client program
"understanding" the structure of the document *a priori*. A web crawler is an
example of a kind of program that might need this manner of flexibility.
Semantic metadata can help a lot in these cases -- cases where we need to
inject some structure into unstructured data.

That's where JMDE comes in. Other metadata discovery engines exist for other
document formats, as well as for natural language documents. As yet, I
haven't found any for dealing with JSON.

License
-------
JMDE is under the MIT License. :)
