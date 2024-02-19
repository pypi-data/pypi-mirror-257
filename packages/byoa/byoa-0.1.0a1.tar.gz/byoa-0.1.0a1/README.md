# byoa

<!-- start elevator-pitch -->
byoa is a command-line utility to Build Your Own Analytic based on metrics and imagery data following your business logic.

* **Create** your own processor from a template
* **Use** the processor in Docker containers or as a simple Python library
* **Deploy** processor in an analytics cluster
<!-- end elevator-pitch -->

## Getting started
<!-- start getting-started -->

### Installation
Install via from PyPI
```
pip install byoa
```

### Create the processor project
Once byoa is installed, create a new processor with:

```
byoa init
```

Several input values will be asked:
- **name** is the display name of the processor
- **slug** is the identifier of the processor
- **repository** is the name of the folder the project will be created in

And voila ! The new project is located in the `repository` folder. You should be able to:
```
cd repository
```

### Building the processor
#### As a Python library
Then build the processor.
As a Python library (wheel):
```
byoa build wheel
```
The wheel file is located in the dist folder. You can then install the library with:
```
pip install path_to_wheel_file.whl
```

#### As a Docker image
If you would rather build a Docker image:
```
byoa build image
```

Then run the image with:

```
byoa run image --mode
```

`--mode` determines the entrypoint used to run the image. For example, `--api` runs the processor as a [FastAPI](https://fastapi.tiangolo.com/) application.

### Deploy the processor
Deploying a processor does several things :
- Registers the processor in an Analytics Cluster (if it is the first deployment)
- Registers the processor's version to deploy in an Analytics Cluster
- Builds and push the processor image in a container registry

The version is set in the `VERSION` file.
You may have to set your Python path (`PYTHONPATH` environment variable) to `src`.

Deploy your processor with the following command:
```
byoa deploy
```

You undo the deployment with the command:
```
byoa delete --version VERSION
```

<!-- end getting-started -->

## Contact
* Report a bug or request a feature: [Issue](https://github.com/GEOSYS/byoa/issues)
* For any additional information, please [email us](mailto:sales@earthdailyagro.com)
* Socials : [LinkedIn](https://fr.linkedin.com/company/earthdailyagro), [X](https://twitter.com/EarthDailyAgro)

## License
Distributed under the [MIT License](LICENSE).
