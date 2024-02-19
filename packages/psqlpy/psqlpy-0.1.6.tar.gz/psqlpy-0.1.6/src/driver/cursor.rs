use deadpool_postgres::Object;
use pyo3::{exceptions::PyStopAsyncIteration, pyclass, pymethods, PyAny, PyObject, PyRef, Python};
use std::sync::Arc;

use crate::{
    common::rustengine_future, exceptions::rust_errors::RustPSQLDriverPyResult,
    query_result::PSQLDriverPyQueryResult,
};

#[pyclass]
pub struct Cursor {
    db_client: Arc<tokio::sync::RwLock<Object>>,
    cursor_name: String,
    fetch_number: usize,
    closed: Arc<tokio::sync::RwLock<bool>>,
}

impl Cursor {
    pub fn new(
        db_client: Arc<tokio::sync::RwLock<Object>>,
        cursor_name: String,
        fetch_number: usize,
    ) -> Self {
        return Cursor {
            db_client,
            cursor_name,
            fetch_number,
            closed: Arc::new(tokio::sync::RwLock::new(false)),
        };
    }
}

#[pymethods]
impl Cursor {
    pub fn fetch<'a>(
        &'a self,
        py: Python<'a>,
        fetch_number: Option<usize>,
    ) -> RustPSQLDriverPyResult<&PyAny> {
        let db_client_arc = self.db_client.clone();
        let cursor_name = self.cursor_name.clone();
        let fetch_number = match fetch_number {
            Some(usize) => usize,
            None => self.fetch_number.clone(),
        };

        rustengine_future(py, async move {
            let db_client_guard = db_client_arc.read().await;
            let result = db_client_guard
                .query(
                    format!("FETCH {fetch_number} FROM {cursor_name}").as_str(),
                    &[],
                )
                .await?;
            Ok(PSQLDriverPyQueryResult::new(result))
        })
    }

    #[must_use]
    pub fn __aiter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    pub fn __anext__(&self, py: Python<'_>) -> RustPSQLDriverPyResult<Option<PyObject>> {
        let db_client_arc = self.db_client.clone();
        let cursor_name = self.cursor_name.clone();
        let fetch_number = self.fetch_number.clone();

        let future = rustengine_future(py, async move {
            let db_client_guard = db_client_arc.read().await;
            let result = db_client_guard
                .query(
                    format!("FETCH {fetch_number} FROM {cursor_name}").as_str(),
                    &[],
                )
                .await?;

            if result.len() == 0 {
                return Err(PyStopAsyncIteration::new_err("Error").into());
            };

            Ok(PSQLDriverPyQueryResult::new(result))
        });

        Ok(Some(future?.into()))
    }

    /// Close cursor.
    ///
    /// # Errors
    /// May return Err Result if cannot execute CLOSE command
    pub fn close<'a>(&'a self, py: Python<'a>) -> RustPSQLDriverPyResult<&PyAny> {
        let db_client_arc = self.db_client.clone();
        let cursor_name = self.cursor_name.clone();
        let closed = self.closed.clone();

        rustengine_future(py, async move {
            let is_closed = {
                let closed_read = closed.write().await;
                *closed_read
            };
            if is_closed {
                return Err(
                    crate::exceptions::rust_errors::RustPSQLDriverError::DBCursorError(
                        "Cursor is already closed".into(),
                    ),
                );
            }

            let db_client_guard = db_client_arc.read().await;

            db_client_guard
                .batch_execute(format!("CLOSE {cursor_name}").as_str())
                .await?;

            let mut closed_write = closed.write().await;
            *closed_write = true;

            Ok(())
        })
    }
}
