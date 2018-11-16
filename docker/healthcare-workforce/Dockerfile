FROM umec/node-python-jupyter:0.3
RUN sudo apt-get remove make -y
RUN sudo apt-get install unzip procps -y
COPY docker-entrypoint.sh /usr/local/bin/
COPY server-install.sh /usr/local/bin/
COPY ui-install.sh /usr/local/bin/
COPY jupyter-start.sh /usr/local/bin/
EXPOSE 80 3000 5000 8888
CMD ["/usr/local/bin/docker-entrypoint.sh"]