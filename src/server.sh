#!/bin/sh
cd /NLP_TOOLS/tool_sets/stanford-corenlp/latest

/etc/alternatives/java -Djava.io.tmpdir=${PROJECT_ROOT}/var/tmp -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 0 2>&1 | tee $SERVER_LOG
