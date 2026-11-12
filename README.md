# Offline translation software QA on standard Windows

This is a small, manually started software compatibility and translation regression project. It tests publicly downloadable GGUF models against original synthetic English text in Simplified Chinese, Malaysian Malay and Tamil. It is not a hosted AI service and does not connect to any customer website.

## Zero-spend configuration

- The workflow uses only the standard `windows-2022` GitHub-hosted runner. GitHub documents 4 CPU / 16GB RAM for standard public-repository Windows runners, with free public-repository compute.
- A job-level public-repository condition is evaluated before allocation; private-repository runs are refused. The bootstrap adds a second public-runner check.
- Manual dispatch only, one job at a time, 75-minute maximum. No schedule, pull-request execution, paid/larger/GPU runner, external cloud account, AI-provider API, subscription or purchase.
- No model caching, artifact upload, package publishing or result commits. Model/runtime files live only on the temporary machine. Small synthetic test results are preserved in ordinary workflow logs, not artifact storage.
- No secrets, customer records, website source, production endpoints or website credentials are included. The workflow token has only repository read permission and checkout credentials are not persisted. Model-child environment variables are restricted to a small OS allowlist and a random local API key.

Official references checked on 2026-11-12:

- [Standard public/private runner specifications](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Actions compute and storage billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

## Models and runtime

`models.json` pins repositories, revisions, file sizes and SHA256:

- Tencent official Hy-MT2 7B Q4_K_M, Apache-2.0.
- Qwen3.5 9B Q4_K_M, Unsloth community GGUF of the official Qwen model, Apache-2.0.

The official llama.cpp b12282 Windows CPU archive is checksum-verified before extraction. No remote Python model code is executed. Model downloads are public and send no AI account token. Once the download is verified, Python inference connections are restricted to loopback. The native model server uses a local file, binds to 127.0.0.1, requires a fresh random key and is placed in a kill-on-close Windows Job Object.

Hy-MT2 uses its verified official 7B template, which differs from its 1.8B template. Qwen uses the embedded model chat template with server reasoning disabled. Raw text, actual hardware, configuration, completion status and timings are recorded. Incomplete answers and failed jobs are never marked semantically accepted.

There are 28 original synthetic cases, up to 84 outputs per model. All brand/location names, news passages, times, quantities and product directions are invented testing data. Instructions inside source text are translated as text, never executed. No external news article text is republished.

## Interpretation and Windows offline delivery

Successful execution is not semantic accuracy. A reviewer must inspect negation, sequence, quantities, names, colour direction, application locations, additions, omissions and natural language usage. There is no claimed accuracy percentage or native-speaker certification.

This validates the Windows software path and cloud-machine observations. It does not guarantee the speed or available memory of a particular customer laptop. A later offline Windows delivery uses downloaded model weights and a local runtime; it has no dependency on this temporary cloud runner or an AI-provider account.

Nothing in this project can approve or publish website content. Any later product integration must have separate human review and explicit publication after acceptable translation quality.

## Running

Use **Actions → Manual free Windows translation QA → Run workflow** and select a pinned model. Avoid adding any secrets, billing features, extra hardware or artifact/cache steps. Result JSON can be reconstructed from the `BENCH_RESULT_*` log frames and verified against the emitted SHA256. Model weights are not uploaded to the repository.
