from requests_cache import CachedSession

session = CachedSession(
    "demo_cache",
    use_cache_dir=True,  # Save files in the default user cache dir
    cache_control=True,  # Use Cache-Control response headers for expiration, if available
    expire_after=120,  # Otherwise expire responses after one day
    allowable_codes=[
        200,
    ],
    match_headers=["Accept-Language"],  # Cache a different response per language
    stale_if_error=True,  # In case of request errors, use stale cache data if possible
)
