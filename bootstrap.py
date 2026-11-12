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

def prepare():
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
    names=['benchmark.py','windows_support.py','models.json','cases.json','bootstrap.py','README.md','.github/workflows/test.yml','.gitignore']
    paths=[root/n for n in names]+[p for p in engine.rglob('*') if p.is_file()]
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
    parser=argparse.ArgumentParser();parser.add_argument('--emit-results',action='store_true');args=parser.parse_args()
    emit() if args.emit_results else prepare()
