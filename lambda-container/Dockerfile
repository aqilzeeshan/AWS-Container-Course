FROM public.ecr.aws/lambda/provided:al2

RUN yum install -y openssl jq && update-ca-trust

COPY bootstrap /$LAMBDA_RUNTIME_DIR/
COPY ssl_tester.sh /$LAMBDA_TASK_ROOT

CMD ["ssl_tester.sh"]
