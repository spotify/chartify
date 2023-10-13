# Security Policy

We commit to publishing security updates for the version of `Chartify` currently
on the `master` branch.

## Expectations
We treat security reports equivalent to a P0 priority level. This means that we attempt to fix them as quickly as possible.
We will release a hotfix for any major security report found in the most recent stable version of our software. 

Any vulnerability reported for any chartify websites like [chartify](https://chartify.readthedocs.io/) does not require a release and will be 
fixed in the website itself.

## Reporting a Vulnerability

To report a vulnerability, please create new issue on the github with a description of the problem,
the steps you took to reproduce the problem, affected versions and any known mitigations.

We should reply you probably sooner.

We use GitHub's security advisory feature to track open security reports. You should expect
a close collaboration as we work to resolve the security vulnerability you have reported. 

You may also reach out to the team via our public [Slack](https://slackin.spotify.com/) chat 
channels.

##  Flagging Existing Issues as Security-related
If you believe that an existing github issue is security-related, we ask that you send an 
email to the maintainers email. The email should include the github issue ID and a short 
description of why it should be handled according to this security policy.

Security reports are not tracked explicitly in the github issue database. 

## Disclosure Process

This section describes the process used by the Chartify team when handling vulnerability reports.

Vulnerability reports are received via the maintainer's e-mail alias. Certain team members
who have been designated the "vulnerability management team" receive these e-mails. When receiving
such an e-mail, one of the vulnerability management team members will:

1. Reply to the email acknowledging its receipt, cc'ing  the other 
members of the team make aware that they are handling the security report. If the email does not describe
an actual vulnerability, the process will stop here.
2. Triage the report to evaluate its impact and if it is a security vulnerability.
3. Collaborate with the appropriate maintainers to ensure that an owner is assigned to the report. 
The owner will drive it through the fix and release process.
4. Work with the maintainers to determine if this security report requires a security advisory.
5. Reach out to the reporter to ask them if they would like to be involved and whether they would like to be credited. 
For credit, the GitHub security advisory UI has a field that allows contributors to be credited.
6. Work with the release and maintainers team to coordinate the publication of the security advisory.
