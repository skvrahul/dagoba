dagoba = require('./dag.js')

V = [ {name: 'alice'}                                         // alice gets auto-_id (prolly 1)
, {_id: 10, name: 'bob', hobbies: ['asdf', {x:3}]}] 
E = [ {_out: 1, _in: 10, _label: 'knows'} ]
g = Dagoba.graph(V, E)

g.addVertex({name: 'charlie', _id: 'charlie'})                // string ids are fine
g.addVertex({name: 'delta', _id: '30'})                       // in fact they're all strings
g.addEdge({_out: 10, _in: 30, _label: 'parent'})
g.addEdge({_out: 10, _in: 'charlie', _label: 'knows'})
knows = g.v(1).out('knows').out().run()                               // returns [charlie, delta]
console.log(knows, 'knows')
