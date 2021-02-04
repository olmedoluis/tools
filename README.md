[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/olmedoluis/pix">
    <img src="images/jpt-icon.png" alt="Logo" width="80" height="80">
  </a>

  <p align="center">
    Pix is a Command Line Interpreter app to use as git in a simple way
    <br />
    <br />
    <a href="https://github.com/olmedoluis/pix/issues">Report Bug</a>
    ·
    <a href="https://github.com/olmedoluis/pix/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

<!-- ABOUT THE PROJECT -->

## About The Project

Pix is a Command Line Interpreter app to use as git in a simple way.

### Built With

- [Python](https://www.python.org/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- python3

Check how to install here [python3_installation_instructions_link](https://www.python.org/)

- pip3

Check how to install here [pip3_installation_instructions_link](https://pip.pypa.io/en/stable/installing/)

### Installation

1. Clone the repo

```sh
git clone https://github.com/olmedoluis/pix.git
```

2. Give Permission to the installer file

```sh
sudo chmod +x ./install.sh
```

3. Run the installer

```sh
sudo ./install.sh
```

<!-- USAGE EXAMPLES -->

## Usage

- In order to see the status:

```sh
px work
```

- In order to add/stage files:

```sh
px add pattern_path_to_the_file
```

It will search for the available files to add/stage and if there is more than one it will ask you which files you want to add/stage.

```sh
px add all pattern_path_to_the_file
```

It will search for the available files to add/stage but it will not ask you to add/stage them.

- In order to remove/un-stage:

```sh
px remove pattern_path_to_the_file
```

It will search for the available files to remove/un-stage and if there is more than one it will ask you which files you want to remove/un-stage.

```sh
px add all pattern_path_to_the_file
```

It will search for the available files to remove/un-stage but it will not ask you to remove/un-stage them.

- In order to reset files as they were:

```sh
px reset pattern_path_to_the_file
```

It will search for the available files to reset and if there is more than one it will ask you which files you want to reset.
This only resets the changes that are non-committed yet and the ones that are not added/staged.

```sh
px reset all pattern_path_to_the_file
```

It will search for the available files to reset but it will not ask you to reset them.

- In order to interact with branches:

```sh
px branch pattern_path_to_the_file
```

It will search for the available branches and then.

```sh
px branch new
```

It will search for the available files to reset but it will not ask you to reset them.

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Luis Olmedo - olmedoluis012@gmail.com

Project Link: [https://github.com/olmedoluis/pix](https://github.com/olmedoluis/pix)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/olmedoluis/pix.svg?style=flat-square
[contributors-url]: https://github.com/olmedoluis/pix/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/olmedoluis/pix.svg?style=flat-square
[forks-url]: https://github.com/olmedoluis/pix/network/members
[stars-shield]: https://img.shields.io/github/stars/olmedoluis/pix.svg?style=flat-square
[stars-url]: https://github.com/olmedoluis/pix/stargazers
[issues-shield]: https://img.shields.io/github/issues/olmedoluis/pix.svg?style=flat-square
[issues-url]: https://github.com/olmedoluis/pix/issues
[license-shield]: https://img.shields.io/github/license/olmedoluis/pix.svg?style=flat-square
[license-url]: https://github.com/olmedoluis/pix/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/luisaolmedo
[product-screenshot]: images/screenshot.png
