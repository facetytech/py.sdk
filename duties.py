# noqa: D100

from duty import duty
from os import walk, path


@duty
def make_pb2(ctx):
    '''Generating Python files from **/_grpc/*.proto files.'''

    for dirpath, dirnames, filenames in walk('.'):
        for entry in filenames + dirnames:
            entry_path = path.join(dirpath, entry)
            if path.isfile(entry_path) and entry.endswith('.proto') and dirpath.endswith('_grpc'):
                ctx.run(
                    ' '.join(
                        [
                            'python -m grpc_tools.protoc',
                            '--proto_path=.',
                            '--python_out=.',
                            '--grpc_python_out=.',
                            entry_path,
                        ]
                    ),
                    title='Generating Python files from **/_grpc/*.proto files.',
                )


@duty
def poetry_login(ctx, source: str):
    '''Login poetry to {source}.'''

    ctx.run(
        f'poetry config http-basic.{source} oauth2accesstoken $( gcloud auth print-access-token )',
        title=f'Login poetry to {source}.',
    )
