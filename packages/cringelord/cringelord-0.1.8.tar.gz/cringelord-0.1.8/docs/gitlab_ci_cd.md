# GitLab CI/CD
This page details the CringeLord CI/CD pipeline. If you need inspiration or a 
good example of how to configure a CI/CD pipeline in GitLab, look no further!

## General
In this section, we'll go over the general properties of the pipeline. 

### Image
GitLab CI/CD uses containers to perform its tasks. For SOC, this is (one of)
the major benefits of GitLab CI/CD over Jenkins. For example, we can use any
image (public or private) to perform our builds. We're not dependent on 
SSC.Computing & Internal Outsourcing to install the tools or OS upgrade we 
require. 

You can specify the image via the `image` keyword (as you might use `FROM` in 
Docker). 
```yaml title="Image Specification"
# .gitlab/gitlab-ci.yml

image: python:3.12 # (2)!
```

1. This is the second comment.
2. As CringeLord is a Python script, it uses the standard base image. Python 
   version 3.12 is the latest release as of this writing. 

### Defaults
You can create a `defaults` section to specify the keywords you want to 
associate with every job (i.e. stages) in your pipeline. 

In CringeLord, we tag all jobs with the tag of our SOC GitLab Runner.
```yaml title="Default Keys"
# .gitlab/gitlab-ci.yml

default:
  tags:
    - soc-runner
```
!!! danger "Don't forget to tag your jobs!"

    Our SOC GitLab Runner is configured so that it only accept jobs and stages
    that are tagged with one of the Runner's tags. If you don't add the 
    `soc-runner` tag, your stage won't be picked up by our Runner. 

### Before
You can specify a script that will run before every job (i.e. stage):
```yaml title="Run Every Time"
# .gitlab/gitlab-ci.yml

before_script:
  - curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash # (1)!
  - source "$HOME/.rye/env" # (2)!
```

1. As CringeLord is managed by Rye, we need Rye for every job in the pipeline.
2. We add  Rye's executables to your path, so you can just type `rye` 
   into the shell to pick up the current virtualenv's Python interpreter.

### Stage Specification and Order
You can specify the names and order of the pipeline stages using the `stages`
keyword:
```yaml title="Specify Stages and Their Order of Execution"
# .gitlab/gitlab-ci.yml

stages:
  - test
  - build
  - publish
  - deploy
```

## Stages
This section will describe the stages of the CringeLord CI/CD pipeline ( at a
high level).

### Test
The `test` stage is responsible for running the script's tests (
who could have guessed?). 

```yaml title="Test Stage"
# .gitlab/gitlab-ci.yml

test:
  stage: test
  script: # (1)!
    - rye sync
    - export PYTHONPATH=$PYTHONPATH:$(pwd)/src
    - mkdir test_reports
    - mkdir coverage
    - rye run pytest
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/' #(2)!
  artifacts: # (3)!
    when: on_success
    reports:
      coverage_report:
        coverage_format: cobertura
        path: test_reports/cov.xml
    paths:
      - coverage!
  rules: # (4)
    - changes:
        - 'docs/**/*'
        - '*.md'
      when: never
    - when: on_success
```

1. Script to run the test. 
2. Regex for extracting the total coverage from a cobertura-formatted test report. 
3. Save the test reports for further reference.
4. We only want to run the tests when changes are made to non-documentation files.

### Build
The build step builds the CringeLord application (i.e. it creates the 
executables).

```yaml title="Build Stage"
# .gitlab/gitlab-ci.yml

build:
  stage: build
  script: # (1)!
    - rye build
  artifacts:
    paths:
      - dist/*
  rules: # (2)
    - changes:
        - 'docs/**/*'
        - '*.md'
      when: never
    - when: on_success
```

1. Use Rye to build the application (which uses Hatchling's build system).
2. As with tests, don't build when only documentation was changed.


### Publish
This stage uploads the artifacts from the build stage to our GitLab 
repositories. 

```yaml title="Publish Stage"
# .gitlab/gitlab-ci.yml

publish:
  stage: publish
  script:
    - twine upload --skip-existing --repository-url https://gitlab.cegeka.com/api/v4/projects/869/packages/pypi dist/*
  variables:
    TWINE_USERNAME: "gitlab-ci-token"
    TWINE_PASSWORD: $CI_JOB_TOKEN # (1)!
  rules:
    - if: '$CI_COMMIT_TAG' # (2)!
```

1. Use the Job's toke to upload to GitLab. This is another reason why GitLab CI/CD is better than Jenkins: availability of pre-defined variables during your pipeline. 
2. Only publish when tags are committed. 

### Pages
This stage deploys your documentation on GitLab pages. 

```yaml title="Pages Stage"
# .gitlab/gitlab-ci.yml

pages:
  stage: deploy
  script:
    - rye sync # (1)!
    - rye run mkdocs build --site-dir public # (2)!
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH # (3)!
    - changes: # (4)!
        - "docs/**/*"
        - "*.md"
  allow_failure: true # (5)!
```

1. We create documentation using MkDocs, which is a dependency managed by Rye. 
2. Build our MkDocs site.
3. Only deploy documentation on commits to the default (i.e. main) branch.
4. Only redeploy documentation when changes are made to documentation.
5. A failure to build or deploy the documentation should not result in a failed pipeline.

## Full Pipeline Config
```yaml linenums="1" title=".gitlab/gitlab-ci.yml"
image: python:3.12

default:
  tags:
    - soc-runner

stages:
  - test
  - build
  - publish
  - deploy

before_script:
  - curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash
  - source "$HOME/.rye/env"

test:
  stage: test
  script:
    - rye sync
    - export PYTHONPATH=$PYTHONPATH:$(pwd)/src
    - mkdir test_reports
    - mkdir coverage
    - rye run pytest
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    when: on_success
    reports:
      coverage_report:
        coverage_format: cobertura
        path: test_reports/cov.xml
    paths:
      - coverage
  rules:
    - changes:
        - 'docs/**/*'
        - '*.md'
      when: never
    - when: on_success

build:
  stage: build
  script:
    - rye build
  artifacts:
    paths:
      - dist/*
  rules:
    - changes:
        - 'docs/**/*'
        - '*.md'
      when: never
    - when: on_success

publish:
  stage: publish
  script:
    - twine upload --skip-existing --repository-url https://gitlab.cegeka.com/api/v4/projects/869/packages/pypi dist/*
  variables:
    TWINE_USERNAME: "gitlab-ci-token"
    TWINE_PASSWORD: $CI_JOB_TOKEN
  rules:
    - if: '$CI_COMMIT_TAG'

pages:
  stage: deploy
  script:
    - rye sync
    - rye run mkdocs build --site-dir public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - changes:
        - "docs/**/*"
        - "*.md"
  allow_failure: true
```