# Offline translation software QA on standard Windows

This is a small, manually started software compatibility and translation regression project. It tests publicly downloadable GGUF models against original synthetic English text in Simplified Chinese, Malaysian Malay and Tamil. It is not a hosted AI service and does not connect to any customer website.

## Zero-spend configuration

- The workflow uses only the standard `windows-2022` GitHub-hosted runner. GitHub documents 4 CPU / 16GB RAM for standard public-repository Windows runners, with free public-repository compute.
- A job-level public-repository condition is evaluated before allocation; private-repository runs are refused. The bootstrap adds a second public-runner check.
- Manual dispatch only, at most two bounded standard/free lanes (12B / other candidates), 75-minute maximum per job. No schedule, pull-request execution, paid/larger/GPU runner, external cloud account, AI-provider API, subscription or purchase.
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

The initial snapshot contains 28 original synthetic cases; later profiles add fresh cases (currently 44, up to 132 language outputs). Each run records its source commit and case set. All brand/location names, news passages, times, quantities and product directions are invented testing data. Instructions inside source text are translated as text, never executed. No external news article text is republished.

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

Execution update: manual standard Windows jobs now have two bounded concurrency lanes (12B / other candidates), so one 12B and one other test can run together. Both retain the same public standard windows-2022 label, 75-minute cap, read-only token, no artifacts/cache/secrets and no paid resources. This only shortens QA waiting time; it creates no ongoing service or schedule. The unstarted serial 12B dispatch was cancelled and replaced; it produced no translations.

`gemma12b` tests Google TranslateGemma 12B using the public Bullerwins community GGUF, exact revision/file length/SHA256 in models.json. Its canonical prompt/turn markers and language codes were inspected directly from that pinned GGUF metadata (HTTP byte-range read, no remote model code). It uses Chinese Simplified, Malay (ms; the pinned template has no ms-MY entry) and Malaysian Tamil locale codes, 2048 context/768 output, greedy decoding and no fitted glossary. It is a separate configured pipeline, not an apples-to-apples base-model ranking.

License: **Gemma Terms of Use, not Apache-2.0**. Gemma is provided under and subject to the Gemma Terms of Use found at https://ai.google.dev/gemma/terms and its referenced Prohibited Use Policy https://ai.google.dev/gemma/prohibited_use_policy. Official base: https://huggingface.co/google/translategemma-12b-it; community quantization: https://huggingface.co/bullerwins/translategemma-12b-it-GGUF. No model weights are redistributed or exposed as an inference service by this repository; the benchmark downloads public weights to a temporary standard Windows runner only. Any future customer distribution must carry the upstream terms/restriction notices and applicable licenses. No API service or AI account is used.


Input validity correction: the first 12B dispatch (43163506495) was stopped because the GGUF requests automatic BOS, which would duplicate the BOS already present in its canonical prompt string. Those partial outputs are configuration-invalid and are excluded from model-quality conclusions. The replacement explicitly tokenizes the canonical text with add_special=false, verifies exactly one initial BOS, and sends integer token IDs, which the native endpoint does not auto-prefix. The local official b12282 vocab-only tokenizer confirmed that Hy7B default/no-BOS sequences are identical, so its ongoing domain run is not affected. No large weights were loaded locally for this diagnostic.


## Sentence and proper-name pipeline experiment

The `hymt7b-segment` profile tests a justified pipeline improvement, not another claim about base-model ranking. It conservatively separates complete English sentences (with abbreviation/decimal guards), protects only the fictional brand/branch names and the named Balayage technique with reversible markers, translates each sentence with generic salon terminology, and restores a name only if every expected marker occurs exactly once. Raw model text, source segments, markers, EOS/truncation/timing/token evidence and final restored text are all retained. No arbitrary translation words are edited or repaired after inference. Marker failures remain incomplete, not accepted. Greedy decoding uses all four standard runner CPUs. Eight additional unseen contrast/quantity/location cases are added before running this profile. Its quality still requires manual semantic review in all three languages.


## Independent larger machine-translation candidate

`madlad7b` evaluates Google's MADLAD-400 7B with the separately identified Heng666 community CTranslate2 INT8 conversion (Apache-2.0). This is not a Google-provided CT2 binary. Required file sizes/SHA256 and revision, plus exact official PyPI Python-3.12 Windows CPU wheels, are pinned in models.json. The SentencePiece model SHA256 matches the official Google repository. Verified official decoder-start ID is 0 and EOS ID is 2; input gets exactly one explicit source EOS because this conversion disables automatic source EOS. Decoding returns EOS for completion evidence. No chat template, glossary, repetition suppression or source rewriting is used; standard beam4 is an independent configured-pipeline test on all 44 synthetic cases. Token sequences, timings and raw translations are recorded.

Only pinned wheel archives from PyPI and native CT2 model data are loaded; no remote Python model code, model-provider API or AI account. All Python sockets are blocked after public downloads. Native inference is CPU-only. The eight source files remain the full public project scope; no dependencies/model binaries are committed or uploaded as artifacts. The large-candidate concurrency lane is shared with 12B, keeping two fixed standard/public/free lanes after the old serial run has exited.

Primary sources: https://huggingface.co/google/madlad400-7b-mt ; https://huggingface.co/Heng666/madlad400-7b-mt-ct2-int8 ; https://opennmt.net/CTranslate2/ ; https://pypi.org/project/ctranslate2/4.6.2/ . Translation quality is still unaccepted until actual three-language semantic review.


MADLAD transport checkpoint: the first dispatch was stopped during download (zero inference outputs), because observed serial throughput could not finish inside the fixed job bound. Four standard HTTP byte ranges are now used with strict 206/Content-Range checks, nonoverlapping writes to one scratch file (no doubled model disk space), bounded retries, immediate rejection of auth/rate errors, and a final full-file SHA256 before loading. No IP/account rotation, rate-limit bypass, paid acceleration, artifact/cache upload or provider API is used. This is a transfer correction, not a translation-quality verdict. The whole download is bounded at40minutes within the75minute job; incomplete scratch is never loaded.


## Context-matched lexicon experiment

The first sentence/name pipeline completed all132 outputs and fixed the unsupported technique ordinal and added scalp restriction, but still translated a hair mask as a face product and cool ash as an attractive colour. The `hymt7b-context` follow-up only supplies terminology when matching source words/context occur. It covers common haircare products, application locations, colour-temperature meanings, ingredients and possibility qualifiers, with face-covering/appliance/calendar/verb safeguards. Its target lexicon is an experimental research glossary, not professionally certified. No raw output words are post-edited; only the documented reversible proper-name restoration remains. Eight new original contrast sentences are frozen before this run (52cases/156 language outputs). These tests support a bounded qualitative decision, not an accuracy percentage or a claim of independent native review.

The first contextual dispatch was stopped during slow serial weight transfer, before any inference. Cloud GGUF downloads now reuse the same four-range, bounded, final-SHA-verified transport already exercised by the MADLAD test. Model bytes, prompts and all52 cases are unchanged. Local resumable downloads keep their previous behaviour. This transfer-only correction is not a quality comparison or acceptance.


## Tamil-specific independent comparison

`sarvam4b` tests Sarvam AI / AI4Bharat Sarvam-Translate (Gemma3-4B based) in Tamil only, using the separately identified mradermacher Q8_0 community GGUF pinned by revision/size/SHA256. It does not support Chinese or Malay and cannot by itself qualify a three-language workflow. All52 unchanged synthetic source cases are used; no glossary, source rewriting, sentence splitting or name restoration. Official system+user messages are rendered into the pinned official/GGUF template, checked equal, then submitted as explicit token IDs with one BOS. Greedy decoding, context2048/output768,4CPU threads. Model-card license is GPL-3.0; the Gemma base has additional upstream terms. No weights are redistributed by this test, and future distribution requires retaining all applicable notices/source obligations. No provider API/account is used. It shares the fixed large-candidate lane with MADLAD/12B, leaving at most two ordinary public standard free jobs active.

Primary sources: https://huggingface.co/sarvamai/sarvam-translate ; https://www.sarvam.ai/blogs/sarvam-translate ; https://huggingface.co/mradermacher/sarvam-translate-GGUF . Support or popularity is not acceptance; actual Tamil semantics must be reviewed.


## Additional independent author-provided models

The owner requests further free offline model evaluation. New candidates are official Qwen3-14B Q4_K_M (9.0GB), official Google Gemma4 E4B QAT Q4_0 (5.15GB), and official Murai Labs Agaram2.5B Q8_0 (2.69GB). Each is Apache-2.0, pinned by author repository/revision/size/SHA256 in models.json, with the original52 synthetic sources unchanged. No prior rejected model is rerun unchanged. The Malaysian-Qwen3 fine-tune was inspected but not selected because its author repository supplies no clear license.

Qwen and Gemma4 test Chinese/Malaysian Malay/Tamil. Agaram is a separate Tamil-only comparison, not a three-language engine. For all supported sources/targets, hand-built prompt bytes are checked equal to both the pinned author and embedded GGUF Jinja templates in a local sandbox. Native completion receives explicit token IDs, add_special=false, with recorded inputs and canonical hashes. Qwen3 non-thinking includes the canonical empty think turn, with recommended non-thinking temperature0.7/top_p0.8/top_k20/min_p0; Gemma4 and Agaram use a documented greedy research configuration. Agaram follows the author's no-system-message guidance and EOS2. Whole original inputs are translated without glossary, source rewriting, segmentation or output post-editing. Context2048/output768,4CPU threads, strict EOS/no truncation.

Only the same eight generic source files are public. At most two fixed public standard Windows jobs run, each bounded75minutes; downloads use verified ordinary ranges and a whole SHA before local CPU inference. No personal AI, provider inference API, secrets, paid/larger/GPU runner, artifact/cache upload or schedule. No private website connection or publication capability. Windows runtime compatibility and quality remain pending actual cloud results; this is not a customer installation or quality certification.

Author sources: https://huggingface.co/Qwen/Qwen3-14B-GGUF ; https://huggingface.co/Qwen/Qwen3-14B ; https://huggingface.co/google/gemma-4-E4B-it-qat-q4_0-gguf ; https://huggingface.co/google/gemma-4-E4B-it ; https://huggingface.co/murai-labs/agaram-2.5b-gguf ; https://huggingface.co/murai-labs/agaram-2.5b-instruct .
