FROM postgres:13.1-alpine AS pgvector-builder

RUN apk add git
RUN apk add build-base
RUN apk add gcc
RUN apk add clang
RUN apk add llvm10-dev llvm10

WORKDIR /home
RUN git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git
WORKDIR /home/pgvector
RUN make
RUN make install

FROM postgres:13.1-alpine
COPY --from=pgvector-builder /usr/local/lib/postgresql/bitcode/vector.index.bc /usr/local/lib/postgresql/bitcode/vector.index.bc
COPY --from=pgvector-builder /usr/local/lib/postgresql/vector.so /usr/local/lib/postgresql/vector.so
COPY --from=pgvector-builder /usr/local/share/postgresql/extension /usr/local/share/postgresql/extension
