#!/bin/bash
cd /NLP_TOOLS/tool_sets/stanford-corenlp/latest

/etc/alternatives/java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 0 2>&1 | tee $SERVER_LOG
