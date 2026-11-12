"""Fetch a pinned public CPU runtime; results go to ordinary workflow logs only."""
import argparse,base64,hashlib,json,os,shutil,urllib.request,zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
URL='https://github.com/ggml-org/llama.cpp/releases/download/b12282/llama-b12282-bin-win-cpu-x64.zip'
SHA='582a5da726b30e0b9e801b4ebd1b85cbe023ca266bdebf6a9d55426c85e57463'

def enforce_free_context():
    if os.environ.get('GITHUB_ACTIONS')=='true':
        event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text(encoding='utf-8'))
        if event.get('repository',{}).get('private') is not False:
            raise RuntimeError('Public repository required; private-repository execution refused.')
        if os.environ.get('RUNNER_ENVIRONMENT')!='github-hosted':
            raise RuntimeError('Only the fixed standard GitHub-hosted workflow is supported.')


def fetch_pinned(item,destination):
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists():
        with destination.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
        if destination.stat().st_size==item['bytes'] and sha==item['sha256']:return
        raise RuntimeError('Existing pinned file mismatch: '+destination.name)
    with urllib.request.urlopen(item['url'],timeout=60) as response,destination.open('wb') as out:
        copied=0
        while chunk:=response.read(1024*1024):
            copied+=len(chunk)
            if copied>item['bytes']:raise RuntimeError('Oversized pinned download')
            out.write(chunk)
    with destination.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    if destination.stat().st_size!=item['bytes'] or sha!=item['sha256']:raise RuntimeError('Pinned download checksum mismatch')

def prepare_ct2(catalog):
    target=root/'ct2-python';target.mkdir(exist_ok=True)
    for item in catalog['pythonWheels']:
        path=root/'wheel-downloads'/item['file'];fetch_pinned(item,path)
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if member.is_dir():continue
                destination=(target/member.filename).resolve()
                if not destination.is_relative_to(target.resolve()):raise RuntimeError('Unsafe wheel path')
                destination.parent.mkdir(parents=True,exist_ok=True)
                with archive.open(member) as source,destination.open('wb') as out:shutil.copyfileobj(source,out)
        path.unlink()
    modeldir=root/catalog.get('modelDirectory','models/madlad7b')
    for item in catalog['requiredFiles']:
        if item['file']!=catalog['file']:fetch_pinned(item,modeldir/item['file'])
    print('Prepared checksum-pinned PyPI CPU wheels and official-matched tokenizer; no large weights loaded.')

def prepare(model=None):
    enforce_free_context()
    path=root/'runtime.zip'
    with urllib.request.urlopen(URL,timeout=60) as response,path.open('wb') as out:shutil.copyfileobj(response,out)
    with path.open('rb') as source:
        if hashlib.file_digest(source,'sha256').hexdigest()!=SHA:raise RuntimeError('Runtime checksum mismatch')
    engine=root/'engine';engine.mkdir(exist_ok=True)
    with zipfile.ZipFile(path) as archive:
        for item in archive.infolist():
            if item.is_dir() or not (item.filename.endswith('.dll') or Path(item.filename).name=='llama-server.exe' or 'LICENSE' in item.filename):continue
            destination=(engine/item.filename).resolve()
            if not destination.is_relative_to(engine.resolve()):raise RuntimeError('Unsafe archive member')
            destination.parent.mkdir(parents=True,exist_ok=True)
            with archive.open(item) as source,destination.open('wb') as out:shutil.copyfileobj(source,out)
    path.unlink()
    catalog=json.loads((root/'models.json').read_text(encoding='utf-8')).get(model or os.environ.get('BENCH_MODEL',''),{})
    if catalog.get('runtimeKind') in ['ctranslate2','marian','m2m100']:prepare_ct2(catalog)
    names=['benchmark.py','windows_support.py','models.json','cases.json','bootstrap.py','README.md','.github/workflows/test.yml','.gitignore']
    paths=[root/n for n in names]+[p for p in engine.rglob('*') if p.is_file()]
    if catalog.get('runtimeKind') in ['ctranslate2','marian','m2m100']:
        paths.extend(p for p in (root/'ct2-python').rglob('*') if p.is_file())
        paths.extend(p for p in (root/catalog.get('modelDirectory','models/madlad7b')).rglob('*') if p.is_file() and p.name!=catalog['file'])
    files={}
    for p in paths:
        with p.open('rb') as source:sha=hashlib.file_digest(source,'sha256').hexdigest()
        files[p.relative_to(root).as_posix()]={'bytes':p.stat().st_size,'sha256':sha}
    (root/'integrity.json').write_text(json.dumps({'runtimeSource':URL,'runtimeArchiveSha256':SHA,'files':files},indent=2),encoding='utf-8')
    print('Pinned official runtime prepared. No account keys or model-provider APIs used.')

def emit():
    for path in sorted((root/'results').glob('*.json')):
        payload=path.read_bytes();json.loads(payload)
        encoded=base64.b64encode(payload).decode('ascii')
        sha=hashlib.sha256(payload).hexdigest()
        print('BENCH_RESULT_BEGIN '+path.name+' '+str(len(payload))+' '+sha,flush=True)
        for index in range(0,len(encoded),3000):print('BENCH_RESULT_DATA '+encoded[index:index+3000],flush=True)
        print('BENCH_RESULT_END '+path.name,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit-results',action='store_true');parser.add_argument('--prepare-model');args=parser.parse_args()
    emit() if args.emit_results else prepare(args.prepare_model)
