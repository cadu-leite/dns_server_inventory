# import pytest
# from get_dns import RackSpaceAccess
# from get_dns import RAXDomains

# class Error(Exception):
#     pass
# class AnyInitilizingError(Error):
#     pass


# def test_get_environment_user(monkeypatch):
    
#     monkeypatch.setenv("RACKSPACEUSER", "top_secret")

#     with pytest.raises(OSError):
#         _ = RackSpaceAccess()

# def test_get_environment_token(monkeypatch):
    
#     monkeypatch.setenv("RACKSPACETOKEN", "top_secret")

#     with pytest.raises(OSError):
#         _ = RackSpaceAccess()

# def test_getenv_ok(monkeypatch):

#     monkeypatch.setenv("RACKSPACEUSER", "x")
#     monkeypatch.setenv("RACKSPACETOKEN", "x")
#     try:
#         x = RackSpaceAccess() 
#     except AnyInitilizingError:
#         pytest.fail("Unexpected error occurred ..")




