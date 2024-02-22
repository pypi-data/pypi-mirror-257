#![deny(missing_docs)]

//! This crate provides the ability to extract a Conda package archive or specific parts of it.

use std::path::PathBuf;

use rattler_digest::{Md5Hash, Sha256Hash};

pub mod read;
pub mod seek;

#[cfg(feature = "reqwest")]
pub mod reqwest;

pub mod fs;
pub mod tokio;
pub mod write;

/// An error that can occur when extracting a package archive.
#[derive(thiserror::Error, Debug)]
#[allow(missing_docs)]
pub enum ExtractError {
    #[error("an io error occurred")]
    IoError(#[from] std::io::Error),

    #[error("could not create the destination path")]
    CouldNotCreateDestination(#[source] std::io::Error),

    #[error("invalid zip archive")]
    ZipError(#[from] zip::result::ZipError),

    #[error("a component is missing from the Conda archive")]
    MissingComponent,

    #[error("unsupported compression method")]
    UnsupportedCompressionMethod,

    #[cfg(feature = "reqwest")]
    #[error(transparent)]
    ReqwestError(::reqwest_middleware::Error),

    #[error("unsupported package archive format")]
    UnsupportedArchiveType,

    #[error("the task was cancelled")]
    Cancelled,

    #[error("could not parse archive member {0}: {1}")]
    ArchiveMemberParseError(PathBuf, #[source] std::io::Error),
}

#[cfg(feature = "reqwest")]
impl From<::reqwest::Error> for ExtractError {
    fn from(err: ::reqwest::Error) -> Self {
        Self::ReqwestError(rattler_networking::redact_known_secrets_from_error(err).into())
    }
}

#[cfg(feature = "reqwest")]
impl From<::reqwest_middleware::Error> for ExtractError {
    fn from(err: ::reqwest_middleware::Error) -> Self {
        let err = if let reqwest_middleware::Error::Reqwest(err) = err {
            rattler_networking::redact_known_secrets_from_error(err).into()
        } else {
            err
        };

        ExtractError::ReqwestError(err)
    }
}

/// Result struct returned by extraction functions.
#[derive(Debug)]
pub struct ExtractResult {
    /// The SHA256 hash of the extracted archive.
    pub sha256: Sha256Hash,

    /// The Md5 hash of the extracted archive.
    pub md5: Md5Hash,
}
