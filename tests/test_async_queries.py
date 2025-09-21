import pytest
import asyncio
from async_context.async_queries import async_fetch_users, async_fetch_older_users

@pytest.mark.asyncio
async def test_async_queries():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    assert len(all_users) >= len(older_users), "All users count should be >= older users count"
    assert all(user['age'] > 40 for user in older_users), "All older users must be older than 40"
