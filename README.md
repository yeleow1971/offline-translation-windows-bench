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


The further `gemma412b` profile tests the official Google Gemma4 12B QAT Q4_0 GGUF,6.98GB, Apache-2.0, exact pins in models.json. This is distinct from the previously rejected TranslateGemma12B. It reuses the same52 frozen original sources, faithful system instruction, greedy native completion, context2048/output768/4CPU threads, with both pinned12B author and embedded templates checked for all156 prompts. No additional source fitting or output editing. Available-memory/full-model runtime and three-language quality remain actual cloud tests, never assumed from file size. Shares the bounded large-candidate free/public lane. Sources: https://huggingface.co/google/gemma-4-12B-it-qat-q4_0-gguf ; https://huggingface.co/google/gemma-4-12B-it .


## Independent HPLT Marian translation comparison

`hplt-ta` tests official HPLT/translate-en-ta-v2.0-hplt_opus (2025,HPLT+OPUS data), English to Tamil only. License CC BY4.0; attribution/source/revision are retained. It cannot by itself qualify a three-language website. Original Marian NPZ (307,935,566bytes), SentencePiece and vocabulary are pinned by exact author revision and whole-file SHA256. The same official PyPI CPU wheels used by the earlier CT2 profile are pinned; no PyTorch, remote model Python code, provider API or personal AI is loaded. Native pinned MarianConverter checks supported architecture and uses float32, with no extra weight quantization. The vocabulary is generated into Marian YAML by exact SentencePiece ID and independently checked before conversion; converted shared vocabulary is checked again. The converter's native zero-start decoder is asserted. This is NOT the earlier MADLAD decoder: HPLT has EOS0/UNK1/noBOS, source EOS is added exactly once by CT2 config, and original inputs do not get explicit EOS. Decoder output includes EOS for completion evidence.

All52 unchanged original English sources are translated in full with beam4,4CPU threads,max512tokens, no glossary/source rewrite/sentence splitting/output editing. Original weights, generated binary/config hashes and token strings are recorded, not published as model files. All Python sockets are blocked after verified downloads, before local conversion/inference. Full-model loading/conversion and semantics must pass actual16GBWindows tests. Fixed standard/public/free manual lane, same75min bound, no paid runner/GPU/cache/artifacts/secrets/schedule or private website connection.

Primary sources: https://huggingface.co/HPLT/translate-en-ta-v2.0-hplt_opus ; https://github.com/hplt-project/HPLT-MT-Models ; https://opennmt.net/CTranslate2/guides/marian.html ; pinned converter source https://github.com/OpenNMT/CTranslate2/blob/v4.6.2/python/ctranslate2/converters/marian.py (sets decoder.start_from_zero_embedding=True).


## Separate target-script constrained experiment

`gemma412b-script` keeps the exact official12B weights, canonical prompt and greedy sampling of `gemma412b`, and adds a native llama.cpp GBNF `grammar` field per completion. It allows ordinary Latin/numbers/punctuation and only the selected Chinese or Tamil script; Malay uses Latin. It does not post-edit text, repair meaning or certify language quality. The original baseline remains immutable at its prior commit. Eight new original synthetic contrast sources are frozen in cases.json before dispatch, bringing this new experiment to60 sources/180 outputs. The same eight public source files are retained. The script-only restriction is motivated by a Chinese output containing Devanagari in the baseline; semantic review must still examine all three languages, including unseen contrasts. The existing baseline lane is reused, preserving at most two standard public Windows jobs and the75minute bound. No private website connection or publication capability.

Native grammar reference: https://github.com/ggml-org/llama.cpp/blob/b12282/grammars/README.md . All scripts are public synthetic research, not a customer installer or an accepted translation model.


## Third evaluation round: larger MADLAD translation model

`madlad10b` is a new10.7B parameter model, not a rerun of the rejected7B. It uses the separately pinned Heng666 community CTranslate2 INT8 conversion of google/madlad400-10b-mt; original model license Apache2.0. This is NOT an official Google INT8 binary or a verified tensor-parity claim. Model file10,730,130,249bytes; SHA/revision/config in models.json. The original author's SentencePiece bytes match; every vocabulary ID is compared, sourceEOS2 and decoder-start0 checked against the pinned official config. Windows uses the same pinned PyPI nativeCPU4.6.2 runtime, beam4,4threads, whole60 frozen synthetic English sources to Chinese/Malay/Tamil; original52 plus8 contrasts frozen previously but not yet run. No glossary/source rewrite/chat prompt/post-editing. All complete model bytes are SHA-checked before loading; local8GB preparation never loads weights. Actual16GB cloud memory/compatibility and semantics are pending, not inferred from weight size. Reuses the existing large lane and unchanged75minute manual standard/public/free limit, at most two jobs, no secrets/providerAI/personalAI/paid machines/cache/artifact/schedule or private website connection/publication capability.

Sources: https://huggingface.co/google/madlad400-10b-mt ; https://huggingface.co/Heng666/madlad400-10b-mt-ct2-int8 ; https://opennmt.net/CTranslate2/guides/transformers.html .


## M2M1001.2B comparison

`m2m12b` tests Meta's larger1.2B model, distinct from the originally tested418M. MIT official model and separately pinned jncraton community INT8 conversion(1.25GB), NOT an original Meta INT8 binary or verified tensor-parity claim. Official SentencePiece/vocab/config/tokenizer files are pinned; all128104 real tokenizer vocabulary entries match converted IDs and all8 padded entries are recorded. All180 source-target encodings compare equal to the installed official Transformers M2M100Tokenizer, without model weight inference on local8GB. The cloud runtime uses only pinned native CT2/SentencePiece/PyPI wheels, not remote Python model code, Torch or a model-service API. English source prefix__en__ + original English pieces + EOS2; decoder startEOS2 and explicit target-prefix__zh__/__ms__/__ta__, removed only as a special language token for decoding. beam5 from official config, outputlimit512,4CPU. Full source/output tokens, generation parameters and hashes are preserved. No glossary/source rewriting/output-word editing. Same60 frozen original synthetic sources, standard public Windows16GB, existing baseline lane,75minute bound/max2jobs/free-only safeguards, no publication capability or private data. Runtime/quality remain actual cloud tests.

Sources: https://huggingface.co/facebook/m2m100_1.2B ; https://huggingface.co/jncraton/m2m100_1.2B-ct2-int8 ; https://opennmt.net/CTranslate2/guides/transformers.html#m2m-100 .


## New27B Qwen3.8 experiment within the16GB cloud limit

`qwen3827b` tests a different, larger Qwen3.8-27B checkpoint, Apache2.0. The pinned Unsloth community UD-IQ3_XXS3bit GGUF is10,934,860,704bytes; no official quantization/tensor-parity claim. Higher3bit files did not leave the same intended OS/runtime margin, so this exact variant is identified rather than called equivalent to full precision. The actual16GB Windows load, available RAM, CPU speed and translation quality must be measured; weight size and local tokenizer checks are not deployment acceptance. No smaller-host override is used. Customer physical16GB installation/performance remains separately untested.

The same60 frozen synthetic English sources and all3 target languages are used. All180 prompts compare byte-for-byte to BOTH pinned author and embedded templates with thinking disabled. The standard Transformers generation-tag extension was needed for template metadata, caught locally before dispatch; it changes no template output. A clearly labelled local metadata-only GGUF surrogate(tensor_count0) verifies canonical first-token248045 using the pinned native tokenizer, without weights/inference on local8GB. Full original GGUF SHA is verified in cloud. Native nonthinking sampling follows the author:temperature0.7/top_p0.8/top_k20/min_p0/presence_penalty1.5/repetition_penalty1. Returned native generation settings, full input IDs and payload hashes are recorded. No glossary, source rewrite, segmentation, target-script grammar or output-word editing. The same official b12282 CPU runtime contains qwen35 architecture support; full-model compatibility remains actual test. Existing free/public standard large lane,75minute bound/max2jobs, no API provider/personalAI/secrets/private code/customer data/cache/artifact/schedule/publication capability.

Sources: https://huggingface.co/Qwen/Qwen3.8-27B ; https://huggingface.co/unsloth/Qwen3.8-27B-GGUF .


## Controlled presence-penalty ablation (2026-11-13)

`qwen3827b-p0` changes ONLY presence_penalty from1.5 to0, retaining the same27B community IQ3_XXS GGUF/revision/SHA, nonthinking template and all60 frozen synthetic sources. All other sampling settings remain unchanged. This is an experimental override, not the author's default nonthinking recommendation. The author notes that higher penalties can mix languages and reduce performance: https://huggingface.co/Qwen/Qwen3.8-27B#best-practices . We test the specific hypothesis that removing this penalty improves faithful terminology, not assume it. Prior18 baseline outputs and failures remain intact. No glossary/source rewriting/segmentation/grammar/output editing; all3 languages must still pass semantic review. Canonical prompt, explicit native IDs, payload hashes and returned native sampling settings are recorded. Same manual/public standard free Windows4CPU/16GB lane,75minute cap, max2jobs, no paid resources/provider APIs/private data/artifacts/cache/schedules/publication capability. Customer physical Windows performance remains unverified. Exactly8 public generic files; no website/protocol source added.


## Two new regional8B candidates; optional Tamil evaluation (2026-11-13)

`apertus8b` is AI Singapore Apertus-SEA-LION-v4-8B-IT, author-published Q8_0(8.57GB), all3 targets. Metadata saysMIT while card body/base sayApache2.0; both permissive provenance notices recorded, no full-precision tensor parity claim. `sailor8b` is Sea AI Lab Sailor2-8B-Chat, Apache2.0 base and mradermacher community staticQ8_0(9.09GB); Tamil is absent from its author continued-pretraining list and onlyChinese/MalaysianMalay are evaluated. Dropping unqualified Tamil is allowed in this revised research scope; neither other language is accepted by that fact. Existing frozen60 generic source texts remain byte-identical. No private source, client data or credentials are added.

Both use exact official/embedded canonical templates and explicit native token IDs (Apertus starts1 exactly once; Sailor ChatML starts151644 with no think prefix). Local preflight validates templates and vocabulary metadata only, not full weights/inference on an8GB host. Greedy temp0/top_p1/top_k20/min_p0/repeat1/presence0 is a declared research profile, not an author-default claim. Whole source plus unchanged generic salon context, no glossary/source rewrites/segmentation/grammar/output edits. Actual Windows16GB CPU model SHA/load/speed and all saved target-language meanings must be checked; normal completion/digits/scripts are not accuracy. Final customer physical Windows installation/performance still requires real-device acceptance. The two fixed free/public/manual bounded lanes and75minute limit remain; no paid/larger/GPU/schedules/artifact/cache/provider APIs/personalAI or website connection.

Sources: https://huggingface.co/aisingapore/Apertus-SEA-LION-v4-8B-IT ; https://huggingface.co/aisingapore/Apertus-SEA-LION-v4-8B-IT-GGUF ; https://huggingface.co/sail/Sailor2-8B-Chat ; https://huggingface.co/mradermacher/Sailor2-8B-Chat-GGUF .


`qwensea8b` adds AI Singapore Qwen-SEA-LION-v4-8B-VL, a different regional Qwen3-VL8B checkpoint trained with Malay/Tamil instruction data. Pinned mradermacher original-profile staticQ8_0(8.71GB), MIT author/community metadata with underlying Qwen3-VLApache2 attribution retained; no full-precision tensor-parity claim. Text-only translation, no image inputs/projector/tools. All180 official/embedded canonical prompt renders and native first-token151644 verified without local full weights. Same frozen60 cases/all3 targets, greedy temp0/top_p1/top_k20/min_p0/repeat1/presence0, no glossary/source rewrite/segmentation/grammar/output edits. Actual16GB Windows load/speed/meaning checks and physical customer installation remain acceptance. Reuses the now-free large lane after the earlier candidate terminates; max2 fixed public/manual free jobs, no paid/GPU/larger resources, personalAI/providerAPI/private data/artifacts/cache/schedule/publication. Sources: https://huggingface.co/aisingapore/Qwen-SEA-LION-v4-8B-VL ; https://huggingface.co/mradermacher/Qwen-SEA-LION-v4-8B-VL-GGUF .
