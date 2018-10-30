FROM umec/node-python:0.1
COPY docker-entrypoint.sh /usr/local/bin/
COPY server-install.sh /usr/local/bin/
COPY ui-install.sh /usr/local/bin/
EXPOSE 80 3000 5000
CMD ["/usr/local/bin/docker-entrypoint.sh"]