# Name of Project

get-external-ip, this is a dynamic DNS updater to run as a container and
update an AWS Route53 record.

The plan is to use API Star to poll an api via the DNS record, should that fail
get external ip from [https://www.ipify.org/](https://www.ipify.org/) and update
the sqlite3 database, then using specific AWS credentials update the Route53 record.

## Getting Started

Clone the repo build the container..

### Assumptions:

* Docker
* Terraform
* Python

### The Makefile

All management is via the Makefile, this is to make the project easy to
transition to ci/cd tooling.

### Description



### Prerequisites

Access to an aws account, docker and packer, etc...

### Installing

Fork then clone the repo, run the make file

```bash
make all
```

## Running the tests

Run tests to ensure that required is installed.

## Versioning

Use [CalVer](https://calver.org/) for versioning. For the versions available,
see the [tags on this repository](<project>/<repo>/tags). 

## Authors

* **John MacTavish** - *Initial work* -
[TechSolX](https://github.com/techsolx)

See also the list of
[contributors](https://github.com/techsolx/get-external-ip/graphs/contributors)
who participated in this project.

## License

This project is licensed under this
[LICENSE](LICENSE) see the file for details

## Acknowledgments

* Stack Overflow for all the other stuff I can't remember.
