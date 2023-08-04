from contextlib import contextmanager
from io import StringIO
import sys
from streamlit.runtime.scriptrunner.script_run_context import SCRIPT_RUN_CONTEXT_ATTR_NAME
from threading import current_thread
import streamlit as st

# context manager to redirect log info in console to streamlit output box

@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, None):
                try:
                    buffer.write(b)
                    output_func(buffer.getvalue())
                except:
                    old_write(b)
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write


@contextmanager
def st_stderr(dst):
    with st.expander('See details'):
        with st_redirect(sys.stderr, dst):
            yield
            
@contextmanager
def st_stdout(dst):
    with st.expander('See details'):
        with st_redirect(sys.stdout, dst):
            yield