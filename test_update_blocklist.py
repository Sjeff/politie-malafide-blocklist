import pytest
from update_blocklist import _is_valid_domain, create_blocklist_content


class TestIsValidDomain:
    def test_simple_domain(self):
        assert _is_valid_domain("example.com") is True

    def test_subdomain(self):
        assert _is_valid_domain("sub.example.nl") is True

    def test_hyphen_in_domain(self):
        assert _is_valid_domain("my-shop.nl") is True

    def test_multiple_subdomains(self):
        assert _is_valid_domain("shop.my-store.co.uk") is True

    def test_spaces_invalid(self):
        assert _is_valid_domain("niet geldig") is False

    def test_colon_suffix_invalid(self):
        assert _is_valid_domain("E-mailadressen:") is False

    def test_single_label_invalid(self):
        assert _is_valid_domain("localdomein") is False

    def test_empty_string_invalid(self):
        assert _is_valid_domain("") is False

    def test_single_char_tld_invalid(self):
        assert _is_valid_domain("example.c") is False

    def test_starts_with_dot_invalid(self):
        assert _is_valid_domain(".example.com") is False


class TestCreateBlocklistContent:
    def test_header_present(self):
        content = create_blocklist_content([])
        assert "[Adblock Plus 2.0]" in content
        assert "! Title: Politie.nl Malafide Handelspartijen" in content

    def test_entry_count_in_header(self):
        urls = ["||example.com^", "||malafide.nl^"]
        content = create_blocklist_content(urls)
        assert "! Total entries: 2" in content

    def test_entries_in_output(self):
        urls = ["||example.com^", "||malafide.nl^"]
        content = create_blocklist_content(urls)
        assert "||example.com^" in content
        assert "||malafide.nl^" in content

    def test_empty_list(self):
        content = create_blocklist_content([])
        assert "! Total entries: 0" in content

    def test_entry_format(self):
        urls = ["||webshop.nl^"]
        content = create_blocklist_content(urls)
        lines = content.splitlines()
        assert "||webshop.nl^" in lines
