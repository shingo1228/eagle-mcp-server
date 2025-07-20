# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### Private Disclosure

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. Send an email to the project maintainers (create an issue with "Security" label for contact)
3. Include as much information as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 7 days
- **Updates**: We will keep you informed of our progress
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days

### Responsible Disclosure

We follow a responsible disclosure process:

1. Security issue is reported privately
2. We investigate and develop a fix
3. We coordinate with the reporter on disclosure timing
4. We release the fix
5. We publicly acknowledge the reporter (if desired)

## Security Considerations

### Eagle App Integration

- This server connects to Eagle App running on localhost
- No external network access required beyond local Eagle API
- No data is transmitted outside your local network

### Configuration Security

- Sensitive configuration should use environment variables
- Never commit API keys or personal paths to version control
- Use `.env.local` for local configuration (git-ignored)

### MCP Protocol Security

- Server runs in stdio mode by default (no network exposure)
- All communications are local between MCP client and server
- No authentication required for local operation

## Best Practices

1. **Keep Dependencies Updated**: Regularly update Python dependencies
2. **Local Operation**: Run only on trusted local machines
3. **Environment Isolation**: Use virtual environments
4. **Configuration Review**: Review configuration before deployment
5. **Access Control**: Limit access to the server and Eagle App

## Known Security Considerations

- Server requires access to Eagle App's API (typically localhost:41595)
- Server has read access to Eagle library metadata
- No write operations are performed on Eagle library
- All operations are read-only except for basic API queries

## Reporting Non-Security Issues

For non-security related bugs and issues, please use the standard GitHub issue tracker.