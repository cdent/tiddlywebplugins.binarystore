
A store for binary tiddlers, layered above other stores.

It's purpose to avoid the unnecessary processing of the `text`
attribute when not neeed. This could save greatly on processing time
and cost.

_experimental_

See: http://cdent.tiddlyspace.com/ShuntedBinaryStore

Process
-------

When a tiddler is `PUT` we know if it is binary. If it is we can store
the text somewhere efficiently and then write a normal tiddler for the
metadata of that tiddler.

When a tiddler is `GET` we can get the metadata from the normal
tiddler and then get the text from the efficient place, only if
needed. We can manage the text in a subclass which treats the Tiddler
`text` attribute as a property.

In our first experiments we will use two layered text stores.
