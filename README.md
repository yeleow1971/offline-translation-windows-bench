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


## Follow-up protocol (12 November 2026)

The initial Hy-MT2 run exposed material terminology/meaning errors and two Tamil token-limit truncations. Its old `finished` flag used an obsolete native response field: treat that flag as unverified in commit b25cb36. Raw output is retained, not rewritten. This revision requires native `stop_type=eos`, rejects context truncation/replacement characters, records the stop reason, raises context/output to 2048/768, and tests the official terminology/background pattern with generic salon terms. Eight fresh synthetic holdouts are added before the domain-profile run. No model is accepted from runtime success, mechanical checks or these fitted cases alone. No website connection/publication capability is added.

Hy baseline and Qwen baseline at b25cb36 use the original 28 cases, 1024 context and 384 output cap. The follow-up uses 36 cases and larger caps, so these are configured pipelines, not a controlled ranking of base models. The glossary is a research candidate, not a professionally certified translation glossary.


## Larger dedicated translation candidate

`gemma12b` tests Google TranslateGemma 12B using the public Bullerwins community GGUF, exact revision/file length/SHA256 in models.json. Its canonical prompt/turn markers and language codes were inspected directly from that pinned GGUF metadata (HTTP byte-range read, no remote model code). It uses Chinese Simplified, Malay (ms; the pinned template has no ms-MY entry) and Malaysian Tamil locale codes, 2048 context/768 output, greedy decoding and no fitted glossary. It is a separate configured pipeline, not an apples-to-apples base-model ranking.

License: **Gemma Terms of Use, not Apache-2.0**. Gemma is provided under and subject to the Gemma Terms of Use found at https://ai.google.dev/gemma/terms and its referenced Prohibited Use Policy https://ai.google.dev/gemma/prohibited_use_policy. Official base: https://huggingface.co/google/translategemma-12b-it; community quantization: https://huggingface.co/bullerwins/translategemma-12b-it-GGUF. No model weights are redistributed or exposed as an inference service by this repository; the benchmark downloads public weights to a temporary standard Windows runner only. Any future customer distribution must carry the upstream terms/restriction notices and applicable licenses. No API service or AI account is used.
