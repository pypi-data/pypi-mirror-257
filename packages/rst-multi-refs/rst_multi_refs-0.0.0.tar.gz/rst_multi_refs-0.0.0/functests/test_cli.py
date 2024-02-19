"""Test cases for CLI testing."""
import subprocess


def test_with_npm():
    """CLI I/O test with ``npm`` role."""
    source = ":npm:`react`"
    expected = (
        "\n".join(
            [
                '<document source="<stdin>">',
                "    <paragraph>",
                '        <reference refuri="https://www.npmjs.com/package/react">',
                "            react",
            ]
        )
        + "\n"
    )
    proc = subprocess.run(
        ["python", "-m", "rst_multi_refs"],
        input=source.encode(),
        stdout=subprocess.PIPE,
    )
    assert proc.returncode == 0
    assert proc.stdout == expected.encode()
