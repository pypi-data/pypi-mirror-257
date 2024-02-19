FROM jupyter/base-notebook

USER root

COPY environment.yml /tmp/.
RUN chmod 777 /tmp/environment.yml

USER jovyan
# setup conda environment
RUN mamba env update -n base --file /tmp/environment.yml
ADD --chown=jovyan:users ./container/prod/start.sh /home/jovyan/.

# copy app file
RUN mkdir /home/jovyan/japper_app
COPY --chown=jovyan:users app.ipynb /home/jovyan/japper_app/.
COPY --chown=jovyan:users app /home/jovyan/japper_app/app

RUN chmod 755 /home/jovyan

CMD /bin/bash start.sh