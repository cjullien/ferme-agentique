#!/usr/bin/env node
'use strict';

require('../src/index.js')
  .main()
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
