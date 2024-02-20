# GitLab Application SDK - Python

This SDK is for using GitLab Application Services with Python.

## How to use the SDK

### Installing the package using pip

To install the package run:

```bash
pip install gitlab_sdk
```

### Using the client

Initialize the client:

```python
from gitlab_sdk import Client

client = Client(app_id='YOUR_APP_ID', host='YOUR_HOST')
```

## Client initialization options

| Option          | Description                                                                                                            |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `app_id`        | The ID specified in the GitLab Project Analytics setup guide. It ensures your data is sent to your analytics instance. |
| `host`          | The GitLab Project Analytics instance specified in the setup guide.                                                    |
| `batch_size`    | Optional. Default `1`. How many events are sent in one request at a time.                                              |
| `async_emitter` | Optional. Default `true`. Use `AsyncEmitter` instead of `Emitter` for non-blocking requests.                           |

## Methods

### `identify`

Used to associate a user and their attributes with the session and tracking events.

```python
client.identify(user_id='123abc', user_attributes={ "user_name": "Matthew" })
```

| Property          | Type         | Description                                                              |
| :---------------- | :----------- | :----------------------------------------------------------------------- |
| `user_id`         | `String`     | The ID of the user.                                                      |
| `user_attributes` | `Dictionary` | Optional. The user attributes to add to the session and tracking events. |

### `track`

Used to trigger a custom event.

```python
client.track(event_name=event_name, event_payload=event_payload)
```

| Property        | Type         | Description                                       |
| :-------------- | :----------- | :------------------------------------------------ |
| `event_name`    | `String`     | The name of the event.                            |
| `event_payload` | `Dictionary` | The event attributes to add to the tracked event. |

## Developing with the devkit

To develop with a local Snowplow pipeline, use Analytics devkit's [Snowplow setup](https://gitlab.com/gitlab-org/analytics-section/product-analytics/devkit/-/tree/main#setup).

To run development libraries, run:

```bash
pip install -r requirements-dev.txt
```

and run:

```bash
make -i python-linter

# for help, run:
# make help
```

## Running tests

To run the test suite, first install the required packages:

```bash
pip install -r requirements-test.txt
```

And then, execute the tests:

```bash
pytest
```

### Developer guidelines

##### Releasing New Versions:

When you want your changes to trigger a new release upon being merged to `master`, your commit message should include specific keywords:

1. Major Release: For backward-incompatible changes that require a major version bump.

   ```sh
   [major] Description of the change.
   ```

2. Minor Release: For backward-compatible new features.

   ```sh
   [minor] Description of the new feature.
   ```

3. Patch Release: For backward-compatible bug fixes.

   ```sh
   [patch] Description of the bug fix.
   ```
