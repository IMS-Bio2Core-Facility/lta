# CHANGELOG


## v3.5.2 (2025-11-09)

### Bug Fixes

- Ensure package build
  ([`cd066d3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/cd066d32d896cd16488701311b44eea52ab51b94))

- Failed pipeline
  ([`a83964d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a83964d5c911098aa3350eb70b4baf460d0b0c27))

- Failed setup
  ([`4195ea3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4195ea345ddf071df8cfc119b40e6ec9e5b768ab))

- Missing change
  ([`7be2d60`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7be2d601611d4eeba8fb621c07ba3cb8dc64891c))

- Nox run
  ([`b1d9150`](https://github.com/IMS-Bio2Core-Facility/lta/commit/b1d9150fb450ed740a4080bf768ca4f2270813ff))

- Poetry publish fail
  ([`ed33430`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ed33430418231efe679ad8d2c2f3e2f50a413a26))

- Release persist credentials
  ([`9346388`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9346388b98dc5d6211d5f9f3ead7dafc3f2a6b63))

- Revert unnecessary change
  ([`3fc488d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3fc488d409b640e55b1cb33c6fbea2213a561827))

- Second try
  ([`025b792`](https://github.com/IMS-Bio2Core-Facility/lta/commit/025b792571144e9e58a94b11f30811603aa2a761))

- Switch to poetry publish
  ([`9f657fd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9f657fd2d933b5fa8fe4145b483b6d7833349987))

- Test change remote origin
  ([`c90ddb7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c90ddb77e4d7ed72192ec7c55092cc02953a39df))

- Try offical action to release
  ([`81645a4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/81645a41da04e3b48f60a4c58630c22824a27772))

### Chores

- Bumping to 3.5.1
  ([`bfa59e7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bfa59e7b67c1dd25c1e27d58433e64c34ae34814))


## v3.5.1 (2025-10-29)

### Bug Fixes

- Vulnerability package upgrade
  ([`8989319`](https://github.com/IMS-Bio2Core-Facility/lta/commit/89893193fd41ffb77835d2a2c0543594a3c9815f))


## v3.5.0 (2025-03-29)

### Bug Fixes

- Add project homepage in poetry config
  ([`4fcd077`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4fcd07756960db238a98977932f8be57d7b74617))

- Attempt to fix pipeline test
  ([`7611075`](https://github.com/IMS-Bio2Core-Facility/lta/commit/761107535cbeed6f3be88f03beef490aba70e052))

- Create jaccard if only needed
  ([`281932c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/281932c97e1d477d2c1ff8a6395104a6a9848ee6))

- Failed pipeline
  ([`80fb68b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/80fb68b8ee6aaed3b7aeb5194a755e0acf7f0e7f))

- Failed pipeline
  ([`3142db1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3142db16000ae6af0fb910e361b86e08efb72324))

- Failed pipeline
  ([`065afa4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/065afa4207cc5e867dc06c99650ca53f1236606f))

- Make it backward compatible with < 3.10
  ([`1f70ad5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1f70ad569b7ae902791bfe2098026ad4a97999f1))

- Python semantic release version on release pipeline
  ([`39f1740`](https://github.com/IMS-Bio2Core-Facility/lta/commit/39f1740feb271953bf560c206b5525f087761809))

- Release pipeline fail
  ([`05a3847`](https://github.com/IMS-Bio2Core-Facility/lta/commit/05a384760e1645d07f5f40fd99cd1873dd6aeed6))

- Remove deprecation action
  ([`6ca82d0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6ca82d09a04007cde93524479719b3878de3c034))

- Semantic_release token config
  ([`c2dcf33`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c2dcf33fe036a936495b7ca759253a3f25f5c232))

- Update poetry.lock
  ([`cf4bbf9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/cf4bbf9d75445d5047caf4342e1894c16b9adb92))

### Build System

- *****: Apply updates across repository
  ([`9f0f913`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9f0f9137cacb82397594ac38873939bd3ec97a57))

- *****: Refactor out jaccard
  ([`e37e323`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e37e323576b3e43e945d638565af81e701026cf6))

To ease maintenance and testing, jaccard has been refactored to the the boolean_jaccard package. As
  this functionality is not directly unique to LTA and may have broader uses, this help minimise the
  code base for the repo.

### Continuous Integration

- **actions**: Introduce composite actions
  ([`5d7d676`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5d7d6766474e3706251eebf186a078c2569635f4))

Refactors out common logic into two actions, one for setting up nox and the other for releasing with
  PSR. This makes code more dry, and also gives finer control over the actions.

- **cicd.yml**: Add single quotes
  ([`f278718`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f278718e160d71c89ffde80c53b735fdd7cce6a2))

Absence of single quotes was breaking parsing

- **cicd.yml**: Adds shell specifications for pst action
  ([`d0f3782`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d0f378214292111c75a44e6c51833bdf5fa91658))

- **cicd.yml**: Correct version specifications
  ([`3655a7c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3655a7c87d49a7479b9bbb883f85632009373001))

- **cicd.yml**: Remove unnecessary quotes
  ([`b491153`](https://github.com/IMS-Bio2Core-Facility/lta/commit/b491153347becc5f6475cd8672b91b3c543eacd5))

These were breaking github actions parsing the file

- **cicd.yml**: Split nox actions
  ([`7a52ec0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7a52ec023b74699fd2b815c0162a120eff4d80a0))

This provides a separate action for formatting that also commits any changed files. Once changed,
  lint, type, and security checks are run before requesting the slow running test step.

- **cicd.yml**: Update psr/poetry
  ([`733d096`](https://github.com/IMS-Bio2Core-Facility/lta/commit/733d096331b05f8aadd1bf5d0a36d624c529c100))

- **docs/requirements.txt**: Add boolean-jaccard
  ([`79078a0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/79078a0daa05ee81c97612056ee2151c9b8a6ce7))

With the refactor to remove boolean-jaccard logic, it must now be manually specified as a dependency
  for building Sphinx with ReadTheDocs.

### Features

- Add merged_lipid_classes
  ([`ae6e64f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ae6e64f07b66f167ffdb3c8ec4e132091f20c838))

- Cluster pattern analysis module
  ([`eac8419`](https://github.com/IMS-Bio2Core-Facility/lta/commit/eac8419b3f22a23a807429a60079ed0c0367cbd9))

- Export full column output
  ([`436f26b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/436f26b084ad1cd373423ab01c905f5a969a323a))

- Save filename change and parameter --savealignfiles
  ([`6cadba1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6cadba19ee7576989f4f26efee13bc7eaadc311f))

### Refactoring

- **data_handling.py**: Typing lints
  ([`d8d1553`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d8d15531261142b4ba6e4b337a49e0c4f96fc7af))

Allows typing.any for kwargs. In the context of writing a wrapper, we can't possibly know what the
  passed kwargs will be type-wise (without specifying the entire signature of the wrapped function).
  As such, we strongly type all known inputs, and allow any for kwargs.


## v3.0.1 (2022-02-15)

### Bug Fixes

- **pipeline.py**: Correct filters of jaccard
  ([`5679713`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5679713f3eeb6cb083cb502b44868c8b018b036d))

Correctly filters lipids by dropping any that are not presetn in either condition being compared.
  Additionally, specifies n as a named parameter to prevent confusion.

Closes #26. Closes #27.

### Refactoring

- **jaccard.py**: Correctly check for None
  ([`22e0d70`](https://github.com/IMS-Bio2Core-Facility/lta/commit/22e0d700cbd37209eaf6db2ebd11543bb50ccd35))

It is more pythonic to check for None with `if x is None`.

See #24.


## v3.0.0 (2022-02-14)

### Bug Fixes

- **pipeline.py**: Correct enfc implementation
  ([`529fa49`](https://github.com/IMS-Bio2Core-Facility/lta/commit/529fa49e083ed0b27287c70f1e818f927956a66f))

ENFC for lipid classes is now calculated on the summed total of all lipids in that class.

BREAKING CHANGE: Prior implementations had calculated the ENFC for class by taking the mean and
  st.dev of the individual lipid ENFC for all lipids in a class. While not incorrect, this was
  inconsistent with prior work of this framework. Closes #23.

- **pipeline.py**: Correct grouped Jaccard calculation
  ([`c2c100c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c2c100c1aef9b29b5b06188bb8c721fde4a1e810))

The pipeline now calculates the Jaccard scores for all pairings, similar to the ENFC calculations. A
  file percomparison is output, and these are saved at outputs/jaccard.

BREAKING CHANGE: Previously, the pipeline only calculated the jaccard scores for a single,
  hard-coded pairing. This has been corrected. All users should update to continue to get the
  correct results.

- **pipeline.py**: Filter jaccard calculations
  ([`ba0f97b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ba0f97bfc258f384186064dd8613af44ff0ac270))

Fixes bug where Jaccard similarity was calculated on any group that was non-zero for any condition
  in all conditions. This is prevented by first subsetting and filtering 0-groups before calculating
  the Jaccard score on remaining groups.

- **run.py**: Correct passing of control
  ([`04d5c5a`](https://github.com/IMS-Bio2Core-Facility/lta/commit/04d5c5a6a7e1b87f4691e74023dad41e835c0470))

Control is now passed as a parameter to init the pipeline, rather than as a parameter to the run
  method.

### Build System

- **pyproject.toml**: Pin numpy to ^1.22.2
  ([`5d2af74`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5d2af743d202e36ccf79e0919fb8d6630989e905))

Security update revealed a number of numpy security issues. To update to 1.22.2 (which has patches
  for all known, we must remove the python 3.7 compatibility. Given that the last bugfix for 3.7 was
  in 2020, this seems a fair trade to keep up to date on the analysis software. Additionally, we
  must pass an ignore to Safety, as their monthly database hasn't updated to show that 1.22.2 is
  patched.

See https://github.com/pyupio/safety/issues/364 and https://github.com/numpy/numpy/issues/19038

### Documentation

- **data_handling.py**: Correct docstrings
  ([`bfadda5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bfadda55ccb0ae09e238e83530a71ad627cbe697))

Ensure that docstrings correctly describe the parameters they handle.

- **README.md**: Add version number disclaimer
  ([`b2b78dd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/b2b78dd6dbf7fecad3c420771a00b1998487f1ef))

Adds a section describing the discrepancies between the academic and software version numbers.

- **README.md**: Update output desciption
  ([`366dd98`](https://github.com/IMS-Bio2Core-Facility/lta/commit/366dd982703c53f5cf0347f3db2bb1173dba7837))

Brings output description inline with updated outputs of the pipeline.

### Testing

- **test_helpers_pipeline.py**: Correct pipeline usage
  ([`d3b3af9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d3b3af9934faad54bd27474ee8b0bae58bc08b0c))

Add necessary parameters to reflect new Pipeline behaviour


## v2.0.2 (2022-01-24)

### Bug Fixes

- **jaccard.py**: Catch zerodivision error
  ([`9278005`](https://github.com/IMS-Bio2Core-Facility/lta/commit/92780057c9283eb81fb71be967786ebd38a4540f))

Under some circumstances, the calculation of p for J can trigger a divide by 0 error. Here, we catch
  those and return np.nan when they occur.

Closes #20.

### Build System

- **poetry.lock**: Update dependencies
  ([`4dc293f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4dc293fa1e6fd19a66b6f1a190991547b043b443))

### Documentation

- **pyproject.toml**: Update classifiers
  ([`f43ccab`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f43ccaba5d71132f27b085e673ab4319bbcb4e3e))

With a more mature project, we can now update the PyPI classifiers to reflect the tool more
  accurately.

### Testing

- **test_helpers_jaccard.py**: Add nan test case
  ([`771a874`](https://github.com/IMS-Bio2Core-Facility/lta/commit/771a87407f31cfa9a2f8cd7a35fd2f7873b57bca))

Adds a test to check that NaN is returned when px and py are both 0


## v2.0.1 (2022-01-24)

### Bug Fixes

- **pipeline.py**: Exclude control condition
  ([`88313ed`](https://github.com/IMS-Bio2Core-Facility/lta/commit/88313ed2011bdbb8e36e8ea9fac478700b3c237c))

Exclude control condition to ensure that a control vs control group is not calculated. Previous
  implementation took all groups, resulting in a non-sensical control vs control fold change.

Closes #19.

### Continuous Integration

- **cicd.yaml**: Update security cache
  ([`248e204`](https://github.com/IMS-Bio2Core-Facility/lta/commit/248e2044c74f8004151f573a9d922184ca7ae35a))

Increases the cache number for the security action. This should re-install all the pythons into a
  virtual env. Not sure why we suddenly started getting random "not local" errors.


## v2.0.0 (2022-01-21)

### Bug Fixes

- **parser.py**: Update default parameters
  ([`878df07`](https://github.com/IMS-Bio2Core-Facility/lta/commit/878df07b5df494c2a95d6f479737b973b66d4a4b))

The default threshold of 0.2 was unusable with fewer than 8 samples.

BREAKING CHANGE: Users should update their configuration files to ensure that they specify 0.2 as
  the threshold if they wish to continue using the old value.

### Documentation

- **LICENSE**: Update copyright year
  ([`d4fd7a0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d4fd7a0e54743c1056e6b8e8b9ea41eb75c3a579))

Happy New Years y'all!

- **pipeline.py**: Update docstrings for new functions
  ([`35e98d0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/35e98d0387bfab0e6b7b59959ce451b2f51682ac))

Clarify that the `run` call calculates all ENFCs.

- **README.md**: Add python installation instructions
  ([`4fc9b83`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4fc9b83a67443349e254237d03e84f2dbd731d8f))

Though a "how to" on installing Python is beyond the scope of this tool, a small section with
  helpful links will help decrease the barrier to usability.

- **README.md**: Enumerate defaults
  ([`3404845`](https://github.com/IMS-Bio2Core-Facility/lta/commit/34048454bd116bf521ce8c02e45a50133b3851b8))

Adds a section enumerating parameters and their default values.

- **README.md**: Update usage instructions
  ([`cdc2f09`](https://github.com/IMS-Bio2Core-Facility/lta/commit/cdc2f09ac306a299f5c27189bff25fb7f045f598))

Updates the rEADME to accurately reflect the new `--control` flag.

### Features

- **cli**: Calculate enfc against control
  ([`f9d7e6b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f9d7e6b7f2548a2afbe2ab2a894fc88134c3935d))

The command line flag has been switched from `--order` expecting a tuple to `--control` expecting a
  str. ENFC is changed to be calculated for all groups relative to this control.

BREAKING CHANGE: Previously, if multiple fold change calculations were desired, the user had to call
  `lta` multiple times. Now, a single call produces all fold change calculations for a set of
  experimental conditions. This feature could have been implemented by having the user specify all
  pairs they were interested in. While this could introduce more flexibility (ie it would allow for
  multiple "controls"), it also introduces more overhead for both the user and maintainer.
  Additionally, for the vast majority of experimental designs, there will be only one control.
  Closes #17.

- **examples**: Provide minimum working examples
  ([`c0575f8`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c0575f8eb3f4825c0e691acfc8b431e4e9a015e2))

Adds a minimum viable data file and configuration file to the repository.

### Refactoring

- **cli**: Migrate tissue to compartment
  ([`5ca9aed`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5ca9aed96cc692226edde90f75a33a3f1e22daef))

Compartment is more in-line with the vocabulary expected by lipidomics analysts, so we migrate to
  ease unerstanding.

BREAKING CHANGE: Current users should update any scripts and configs to use the new `--compartment`
  flag rather than the existing `--tissue` flag.

### Testing

- **test_parser.py**: Correct usage message
  ([`e4ec058`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e4ec0587881a7f457a7a21f3e84f2468284d1c8f))

Updates the usage message to reflect new command line flags.

### Breaking Changes

- **cli**: Current users should update any scripts and configs to use the new `--compartment` flag
  rather than the existing `--tissue` flag.

- **parser.py**: Users should update their configuration files to ensure that they specify 0.2 as
  the threshold if they wish to continue using the old value.


## v1.0.0 (2022-01-07)

### Documentation

- **README.md**: Update usage for new flags
  ([`75772f7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/75772f7b81f6bf518b9e5cc55656b5a0740f5dda))

Expands on usage of new flags, and provides more detailed explanations of the expected data
  structure.

### Features

- **cli**: Change phenotype to group
  ([`6b91841`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6b918419e88136e2a47edccb65a0ff31cbace70e))

After feedback from users, it was decided that the "phenotype" flag was not intuitive as to its
  purpose. THis flag has been renamed "group".

BREAKING CHANGE: Change "phenotype" to "group". Existing users will need to make sure that any
  scripts and config files use this new flag.

- **cli**: Generalise data reading
  ([`d5ce9f5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d5ce9f594ff3380ab4cc6cd77fd3f64113530173))

By allowing the user to specify the number of rows in the metadata and the name of each field, it is
  possible to greatly increase the flexibility of the data read in. Additionally, this structure
  should ease future maintenance should the expected data input change or should more fields be
  required.

BREAKING CHANGE: This introduces 2 new command line flags and changes how the data is processed.
  Past scripts are not guaranteed to run correctly - unless, by chance, they used the defaults - so
  a breaking release is required.

### Testing

- **test_helpers_data_handling.py**: Test new data constructor
  ([`f89cef5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f89cef57deba8e33eab1766dcb021f0cbd5e77b6))

Modifies the existing test to reflect the new structure of the data constructor.

- **test_helpers_pipeline.py**: Correct initialisation parameters
  ([`705fb4b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/705fb4bf3947a54e13f8af0a3f2cc3237d90bc00))

Corrects calls to Pipeline to reflect the new data processing format.

- **test_parser.py**: Correct for new flags
  ([`8a9d46d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/8a9d46d02f4ee555ee56fe2ce51ae54f33b2c811))

Modifies existing test to accurately reflect the new flags.

### Breaking Changes

- **cli**: Change "phenotype" to "group". Existing users will need to make sure that any scripts and
  config files use this new flag.


## v0.12.5 (2022-01-04)

### Bug Fixes

- **lta.py**: Remove colons from filenames
  ([`3e4388c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3e4388cfcc5c906ac384195c17588dd6edd0a53f))

Colons are incompatible with Windows files, so they cannot be used in the default log file if we
  desire to remain OD agnostic. Here, they are replaced with dashes.

This also revealed some interesting type errors that have been corrected by a forced cast on the
  handlers.

### Build System

- **repo**: Update dependencies
  ([`65b463a`](https://github.com/IMS-Bio2Core-Facility/lta/commit/65b463a8bd0c47479261c28084cc9f30f09a97cc))

### Continuous Integration

- **cicd.yaml**: Cache on poetry.lock
  ([`b849416`](https://github.com/IMS-Bio2Core-Facility/lta/commit/b8494161f6022f45a2f92c1516d5d68a1e6fbdb0))

Caching on pyrpoject.toml is incorrect, as it does reflect any updates in the lock file. Here, we
  switch to caching on the lock file, to ensure that the most up-to-date deps are always used.


## v0.12.4 (2022-01-04)

### Bug Fixes

- **pipeline.py**: Respect metadata locations
  ([`e906e87`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e906e87816305e071fc47fe6189b817095b08959))

Previously, the call to construct the necessary dataframe had ignored any passed in metadata
  locations. Now, these locations rare referenced in construction, insuring they are available to
  all future methods.

### Continuous Integration

- **cicd.yaml**: Cache pip
  ([`cbbcc17`](https://github.com/IMS-Bio2Core-Facility/lta/commit/cbbcc179975231e93b7ed47c2585fb881eb896b2))

Provides a cache for pip using the versions of Poetry and PSR as the key.

Though caching could be performed with the 'setup-python' github action, that requires a
  requirement.txt file be present.

- **cicd.yaml**: Specify versions as EnvVars
  ([`a929511`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a929511aa6f14cada2bc459a796f060c0b3e6a09))

The most efficient way to use the PSR/Poetry versions for caching has those variables stored as an
  EnvVar. This also simplifies the logic in a few places in the script.

### Documentation

- **README.md**: Update badges
  ([`57718d4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/57718d41d7a1b49e70ec9fb58c0f32b76b8ea9e2))

- **repo**: Use Traffic throughout
  ([`af3c4d1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/af3c4d1554215251b8a4432db3b8a1aba4d1a1e7))

Previously, Trafficking and Taffic had been used in the name of the software interchangeably. To
  standardise and avoid confusion, this has been unified to Traffic in all cases.


## v0.12.3 (2021-12-23)

### Bug Fixes

- **pyproject.toml**: Correct included packages
  ([`d603a6c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d603a6c904c494b480e2b5daa14b1fc267ab1cec))

Since we must use a different name for the overall package, the package to include must be manually
  specified.

- **pyproject.toml**: Correct version number
  ([`0b01aea`](https://github.com/IMS-Bio2Core-Facility/lta/commit/0b01aea41f8cab8a61f4d2d1b85cd864f04bb656))

While fixing merge conflict, the version number was accidentally reverted an increment. This has
  been corrected.


## v0.12.2 (2021-12-23)

### Bug Fixes

- **repo**: Support python3.10
  ([`0edba28`](https://github.com/IMS-Bio2Core-Facility/lta/commit/0edba28f5bf7291379aa4f59b9faee279f5ae39b))

As Python 3.10.1 has released, and as pandas and numpy are now 3.10 compatible, we add support for
  python3.10.

Pre-commit and ReadTheDocs now uses py3.10 as default. Nox includes py3.10 in its matrix, and
  defaults to py3.10 for steps only run in one version. Pyproject.toml now explicitly states python
  versions. Also, though is technically a build release, I'm tagging as a fix to trigger the initial
  public release to pypi.

### Build System

- **cicd.yaml**: Correct action version
  ([`9188f35`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9188f359a52ec7b0cab2c17e5aaa4d6f985d9f60))

Erroneously changed the version number of the install-poetry action. This is now corrected.

- **pip**: Update dependencies
  ([`62eef11`](https://github.com/IMS-Bio2Core-Facility/lta/commit/62eef11583a78b46e8ad7ca5694142579017a16b))

- **poetry**: Update dependencies
  ([`639c119`](https://github.com/IMS-Bio2Core-Facility/lta/commit/639c11930a007518f7f21ec2c895258516b995eb))

- **pyproject**: Update dependencies
  ([`34e40b5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/34e40b5e4f72358a166708645af5504da16bf525))

Several dependencies (notably flake8) had major releases. These have been tested and incorporated,
  where apropriate.

Some consideration was given to upgrading to python 3.10; however, the current lack of wheels for
  pandas and numpy makes the install times intolerably slow and inconsistent. We will wait for the
  first minor release (at least) before that change.

- **pyproject.toml**: Change prackage name to LipidTA
  ([`742a039`](https://github.com/IMS-Bio2Core-Facility/lta/commit/742a0399b384d9536f635bc0200e9c5ac8aa93a8))

According to PyPi, LTA is too close to existing package names for us to use. Thus, we change the
  name to LipidTA.

### Continuous Integration

- **actions**: Configure PSR to release to PyPi
  ([`a482666`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a482666254008e3f559599a3baca646bd600ea67))

With the upcoming public release of the project, a deployment to PyPi is now necessary. Additional
  variables are now defined, and will be sone on Github as well.

- **actions**: Implement caching for actions
  ([`d958891`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d9588913011175bd268bc31ceb083fc0a71aad88))

Where possible, caching is used with nox to reduce action run-time. Here, it is implemented for
  linting, formatting, and security checks.

It is difficult tod ecide what the best way to implement this for testing is. Since I use nox to
  spin off eavh python version, and then poetry to install the project, any existing virtualenvs get
  clobbered by poetry on the install.

- **cicd.yaml**: Update Poetry version
  ([`2f031e1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2f031e11540c4d7cf7b878f353f4149a49560ca2))

Installing packages in py3.10 with poetry < 1.1.12 triggers an obtuse JSONEncode warning. This was
  resolved in the most recent version.

### Documentation

- **docs/index.md**: Correct badges
  ([`1f3685e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1f3685ea9056496c09f62a62b99d177a337d20c2))

Badges on the index now accurately reflect the badges in the README

- **README**: Add future work
  ([`1304204`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1304204d6de27b7c2fe05fd34d27fc53ccb71751))

Adds a future work section to the README to give a sense of project direction to users and
  contributors.

- **README**: Add links
  ([`f26fe30`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f26fe3005b35541c6cf36b5ca880b98239f7f688))

Add links for ReadTheDocs and PyPi. As the package is not yet properly deployed to PyPi, the latter
  may change.

- **README**: Update project name and status
  ([`85e235c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/85e235cbf8f70accf2041cf9d6ecc1c675cd4414))

The status of the project had been erroneously given as "Planning phase". It is now update to
  reflect its active development.

- **readthedocs**: Specify build dependencies
  ([`61837c3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/61837c33f902d89c2b0d7d35ef23a5635e67d743))

Since MyST parsing is being used, we must specify custom build dependencies. This requires a
  requirements.txt and a ReadTheDocs configuration.


## v0.12.1 (2021-09-16)

### Bug Fixes

- **data_handling**: Report senseless FC as 0
  ([`1e0ae79`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1e0ae79ef81452441f1b7bfb1c3f606364694d99))

For fold change to be biologically meaninful, then both values must be non-0. After division with
  pandas, x/0 will be inf or -inf and 0/x will be 0. These values are now changed to NaN and
  propagated down.

Closes #4

### Documentation

- **README**: Document NaN's in output
  ([`4ebc261`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4ebc2613cea1e47f2d16568d6a427f433a8f7c1c))

Documentation now correctly references NaN's in ENFC output.

See #4


## v0.12.0 (2021-09-16)

### Bug Fixes

- **logging**: Add logging for data_handling
  ([`73a2aa3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/73a2aa3329b30998c4c16ac9b738b31e87d21085))

- **logging**: Add logging for Jaccard
  ([`a35e851`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a35e8519f036a0911ce789467494cef7f7ee8a45))

- **logging**: Add logging to pipeline
  ([`3af0c53`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3af0c5368877689a655ce2919c2b42ad01496c6f))

- **logging**: Correct use of logger
  ([`9b332b3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9b332b3579a32a62a7e1ccc994a5705d9c430d36))

Previously, the logging had occurred from the root, rather than from the child instance. This has
  been corrected.

- **logging**: Respect verbosity flag
  ([`5373dd2`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5373dd2447e2cad2b749448de4242632c2ba824f))

The CLI now respects the verbosity flag for increasing/decreasing the logging output.

- **pipeline**: Calculate Jaccard similarity
  ([`4b21ade`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4b21adea2dfc9b4fabe20bff646b2ef1b9bd0cb7))

Switch from output Jaccard distance to Jaccard similarity, as expected to allign with older
  versions.

Closes #2

- **pipeline**: Change output file names
  ([`3b9bdbe`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3b9bdbe9c6a2a2df798f5522ac5e5ab483af1ed6))

Previously, the output file names were difficult to understand and did not provide an intuitive
  understanding of their contents. The new names should allow users - even those unfamiliar with the
  analysis - to understand the contents of the output files.

Closes #3

### Build System

- **deps**: Update dependencies
  ([`7641d8d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7641d8da1e11ff474a70457e8b4bc01bff3d8192))

### Documentation

- **README**: Update file name output
  ([`3e2c1df`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3e2c1df3af86fd9d00a10721d263e05fce05a68e))

See #3

### Features

- **logging**: Add logfile option
  ([`2d0bd60`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2d0bd60ce3cf619a39a4b4c6c6821b7576ca470a))

Users can now specify where they would like the log output to go. Specifying term pipes to StdOut,
  and multiple locations may be specified.

- **logging**: Introduce logging support
  ([`431822a`](https://github.com/IMS-Bio2Core-Facility/lta/commit/431822a1136a25483c799a21d841c6ae3fe96a21))

Introduces basic logging support. Full support of a cumulative verbosity flag and a logging in all
  modules will follow.

### Testing

- **unit**: Support logging
  ([`5cd62b9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5cd62b9958c84d51d696fc32b5fc2a3b6e48c2bf))

Use the provide caplog fixture to capture the newly configured logging.


## v0.11.1 (2021-08-26)

### Bug Fixes

- **data_handling**: Respect axis in enfc
  ([`2d727f7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2d727f716c06e972e4228f2932f572d5ed16b015))

Previosly, helpers.data_handling.enfc did not take into account the axis when slicing for division.
  This has now been corrected.

### Testing

- **unit**: Add tests for enfc
  ([`7059844`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7059844576da1620c164d8a9777f46a6a86ea9be))

Adds tests for lta.helpers.enfc

- **unit**: Test construct_df
  ([`3702d18`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3702d183777cf297c3a74332158585b0f322485b))

Adds unit tests for lta.helpers.data_handling.construct_df. Mocks pandas.read_csv, as we have no
  need to test that, just that it adds names correctly.


## v0.11.0 (2021-08-26)

### Documentation

- **pipeline**: Document summary files
  ([`700c8fb`](https://github.com/IMS-Bio2Core-Facility/lta/commit/700c8fbb63e45d2dc4fb465f179d840652bef419))

### Features

- **pipeline**: Output summary files
  ([`2e51efd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2e51efde9e30c7ffc66b236c847ea0a77951b935))

The pipeline now outputs summary files for lipid types and counts, to help ease processing by
  humans.

- **pipeline**: Summary jaccard output
  ([`742dde1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/742dde161ad9c25926faafe56d66e5ef9c85d6b1))

The pipeline now also provides a summary Jaccard distance file.

- **pipeline**: Support summary enfc
  ([`e927354`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e927354caf4709f9a65eb1a5bb22b10ea90bcfda))

Pipeline now produces a summary ENFC and ENFC_grouped output.

### Refactoring

- **pipeline**: Remove unnecessary file writes
  ([`9f68f0d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9f68f0dc590f0f9f012c3602fddb524d0164080c))

With new summary results, it is no longer necessary to write every combination. This eliminates IO
  calls, improving performance (~1s)


## v0.10.1 (2021-08-25)

### Bug Fixes

- **repo**: Fix build failures
  ([`9ced474`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9ced474825e59ae8cbacc20957917be16913b60d))

There seems to be no good way to use tmp files on windows with Github actions. Bypass by mocking.

### Continuous Integration

- **actions**: Set tmpvar
  ([`bc294f4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bc294f49cae59172f36d90b3556d691b330cc887))

The tmpdir is not correctly set within python on windows in Actions. To circumvent this, we specify
  the tmp location, but only on the windows section of the matrix.

### Documentation

- **command**: Document unified input
  ([`58592ce`](https://github.com/IMS-Bio2Core-Facility/lta/commit/58592ce4ba844409030619c531aee7ed0500dae1))

Insures that the command and parser documentation accurately reflected the new unified input csv.

- **conftest**: Add conftest to sphinx
  ([`e2d9174`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e2d9174664c77d0cd946fdde5dc9660981d00c9e))

- **helpers**: Update docs to unified input
  ([`f94996c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f94996cbf937649df8cb6517fbc36de9e36d6f57))

Just insuring that the helpers sub-package accurately reflects new usage for the unified input file.

- **README**: Reflect unified input file usage
  ([`c7b18e9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c7b18e906f5087a605326fd031caf0e598c5c652))

### Refactoring

- **conftest**: Remove superfluous fixtures
  ([`1905c0b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1905c0bef70bca8a81d5f19dc206d54a342b718d))

Removes the (now) un-needed tmp_folder fixture.

- **data_handling**: Support single input file
  ([`a3412b2`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a3412b26e2185d998376c9f6c024c0be4c4096fd))

Begins refactoring towards single input file. This step adds the necessary additional groupings to
  the data handling module, as well as changing the input to a single file for the pipeline.

- **pipeline**: Support unified input for A-lipids
  ([`ea6627a`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ea6627af17d2203129a1736ae22d054937ef2b21))

- **pipeline**: Support unified input for B-lipids
  ([`4e57c0b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4e57c0bce4bb26e3a40c49b87bccfba116ca0488))

- **pipeline**: Support unified input for ENFC
  ([`a9735aa`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a9735aaa556ef9c9727c44cf7e71c3ea5cf20f97))

- **pipeline**: Support unified input for N-lipids
  ([`bc4096c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bc4096ccf766b24cb21f3d4049176fb4a4c2af4d))

### Testing

- **unit**: Correct parser output
  ([`b51a3c7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/b51a3c7868bf8479100034b1b389f15d30626187))

- **unit**: Fix not_zero tests
  ([`df184bf`](https://github.com/IMS-Bio2Core-Facility/lta/commit/df184bf5f4691349978517accfe7d6fe660d1376))

These tests now correctly reflect the new parameters and slightly altered usage of this function.

- **unit**: Introduce tmp_folder fixture
  ([`3f825d6`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3f825d61f9526fb278b64f6b661b4a55f54d1fa6))

Github actions and Windows don't get along well for tempfiles don't get along well. The errors all
  relate to permissions denial for the default tmp location. We circumvent this by creating a local
  tmp_dir fixture, using yield to insure teardown.

- **unit**: Remove superfluous tests
  ([`7ab1b02`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7ab1b028fff250a578dbdc4184f0d4aabb1654f3))

dh.get_unique_levels has been factored out of existence, so it does not need to be covered.

- **unit**: Update error checks
  ([`5f0139d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5f0139dca67e6b575110b3519b51d2d6fdc9d7c0))

Updates unit tests for pipeline to check for the appropriate errors.

- **unit**: Use manual tmpdir
  ([`ab59e7f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ab59e7f6d10b42f2e289a8d54560ad19c9b46f52))

The pytest tmp_dir fixture has some OS dependent issues - it gets cranky with Windows. To this end,
  we use the input pathlib and tmpfile modules to create a more OS-independent test.


## v0.10.0 (2021-08-20)

### Bug Fixes

- **command**: Order is now user option
  ([`7aa7413`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7aa741393a394bca56699b8e1cede06d1401266c))

Order is no longer hard coded into the CLI, and can be passed as flag to command.

- **parser**: Do not specify nargs
  ([`41ec8fd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/41ec8fda00037fd2e99a5df74ad0805bc7ff8aaf))

Unless n > 1, it is more straightforward to not specify. That way, a bare value is return rather
  than a list of length 1.

- **parser**: Reduce boot-reps
  ([`5e339fb`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5e339fbcef5971e14f27823509439fac4d59fe94))

Reduce replicates to 1000 for speed.

### Documentation

- **enfc**: Add support documentation
  ([`c1eb26e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c1eb26ed22e53a163e9755f44de4aec41c32d48b))

Documents ENFC output in the README, as well as provide docstrings in the code.

### Features

- **data_handling**: Calculate enfc
  ([`e7c28af`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e7c28af36730b913ef8fb648e9087256fefe19a9))

Calculate the error-normalised fold change over a given set of lipids.

- **pipeline**: Calculate enfc
  ([`05ecf05`](https://github.com/IMS-Bio2Core-Facility/lta/commit/05ecf05fe6ab3264ed110950eb97055ccba23b70))

The pipeline now calculates ENFC, in addition to the ANBU lipids.

### Refactoring

- **pipeline**: Story raw and binary
  ([`28303d7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/28303d7884b3abfca641385309a55509bbf0d968))

The actual count data is necessary for ENFC, and it should be filteres as well. Since the already
  calculated binary data does this, we now store both, rather than binary only.

### Testing

- **unit**: Correct usage
  ([`a762e3d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a762e3d28498d80a1e28701efb193ca50930b801))

Updates parser tests to confirm new options.


## v0.9.0 (2021-08-19)

### Build System

- **deps**: Dependency updates
  ([`0440550`](https://github.com/IMS-Bio2Core-Facility/lta/commit/0440550085ea5dc1ab3d02c02e2fca61ed6c6b87))

- **deps**: Support ConfigArgParser
  ([`436e5e2`](https://github.com/IMS-Bio2Core-Facility/lta/commit/436e5e29bb3173f7b70e7266dee2d2db194af05d))

ConfigArgParser is a drop in replacement for ArgParser that allows for support of config files and
  envvars with minimal overhead.

### Documentation

- **data_handling**: Add docs for data-handling
  ([`5a52bd0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5a52bd0c8445b0b58330c977dac7e39a021cba8a))

Sphinx now build documentation for the data_handling module.

- **README**: Document all options
  ([`8c8ee48`](https://github.com/IMS-Bio2Core-Facility/lta/commit/8c8ee48e1733d2618631e425a1013029021fb3dd))

Prior documentation left out the --phenotype and --tissue flags

- **README**: Document config file
  ([`b05f8c9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/b05f8c9325eeedba3c78771eb0fe293e575c78e6))

Provides documentation explaining the use of the config file.

- **README**: Document output of analysis
  ([`17a02e8`](https://github.com/IMS-Bio2Core-Facility/lta/commit/17a02e814c4b848b7de07612507c25dfa7825048))

Provides description to the README that explains the file output of running the analysis.

### Features

- **parser**: Add phenotype and tissue flags
  ([`2acbcc7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2acbcc76fd8ed868304fd3c53afc52dff00a5e45))

The user may now specify where the relevant metadata is stored as an option to the parser.

### Refactoring

- **parser**: Beautify help documentation
  ([`578ba21`](https://github.com/IMS-Bio2Core-Facility/lta/commit/578ba21f8c24636d14d3f3b7caa573ef6b28dc14))

Changes the default help formatter and move options around in order to make the help message more
  readable.

### Testing

- **unit**: Correct parser output
  ([`ad8eeab`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ad8eeab4c6b0c0c20c55f0ee1366db8ed7338b28))

Corrects flags in the parser unit test.


## v0.8.0 (2021-08-19)

### Bug Fixes

- **pipeline**: Capitalise tissue names
  ([`06294fd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/06294fdbd6e4b37827e30445d7698c2c676d585b))

All tissues are now capitalised when referenced in file names.

### Features

- **pipeline**: Support N-lipids
  ([`9f0abbb`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9f0abbbc4e905f521a60e8b65dbe4dcc1e7a7d18))

N-lipids are those lipids found only in N tissues. Thus, N1 lipids are the same as U lipids and N2
  lipids may be seen as a subset of B lipids. Future features will use these lipids to perform
  pathway analysis.

### Refactoring

- **pipeline**: Return dict of dataframes
  ([`ca4cc36`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ca4cc36e770e06651bf68901a6958503c9d9376f))

All lipid finding methods now return dictionaries of dataframes, rather than modifying internal
  state.


## v0.7.0 (2021-08-18)

### Features

- **pipeline**: Split b-lipids
  ([`9254797`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9254797220ee78147081c00129024e6da34d3f15))

As all a-lipids are, by definition, b-lipids, they can clutter analyses. Here, they are split into 2
  sub-groups. B-picky (or Bp) are those B-lipids that are NOT A-lipids, while B-consistent (Bc) are
  those lipids that ARE A-lipids.


## v0.6.1 (2021-08-18)

### Bug Fixes

- **data_handling**: Correct column/index check
  ([`bf143f1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bf143f1bf6f978e59459a35d984e84735b5bd769))

Previously, get_unique_levels checked the index regardless of axis. This has now been corrected.

- **pipeline**: Generalise _split_data level
  ([`9fb0c7e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9fb0c7e12393cc00dff0f17896adb5ca7ca97f3f))

pipeline._split_data now searches the passed level, rather than requiring a hard coded location.

- **unit_tests**: Use binary_df fixture
  ([`46875fa`](https://github.com/IMS-Bio2Core-Facility/lta/commit/46875fa9ced48594012a3b8ef3831786e3d2c68c))

With this fixture, the number of dimensions in the final df can be accurately tested.

Closes #1.

### Build System

- **deps**: Add typing_extensionc
  ([`bab8853`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bab88536f9b115278221e7c687b7fb7d490b93a3))

Typing extensions is necessary for python < 3.8 to support the Literal type.

### Continuous Integration

- **pyproject**: Ignore import for coverage
  ([`6051a67`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6051a6761b20a48ccdd25c20350de9d9aa2d63c3))

Coverage was complaining about failed coverage for a python version dependent import. This obviously
  erroneous (if the code runs, the import worked), so we ignore the offending lines.

### Refactoring

- **conftest**: Adds defaults to fixtures
  ([`642b53d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/642b53d4b838d8582fd72b2ee2399827c6458aaa))

Adds default parameters to the create_df fixture.

- **data_handling**: Add data_handling module
  ([`7ade01e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7ade01e0bb3e1fb1c9da567f08b59ad4e867aac8))

Refactor all data_handling out of pipeline to allow for increased test coverage.

- **pipeline**: Support data_handling
  ([`75a88fc`](https://github.com/IMS-Bio2Core-Facility/lta/commit/75a88fcb42519f3bea024caa82a98b168602aabc))

Refactors the pipeline to support the new data_handling module.

### Testing

- **conftest**: Add binary_df fixture
  ([`ff0f681`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ff0f6813042ba75a856ed23d1845ecfda7e8ee40))

Adds a binary df fixture with known distributions of 0s and 1s, allowing for confident statements
  about filtering.

See #1.

- **conftest**: Add create_df fixture
  ([`1de82c4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1de82c41f002ed2e230abe8aeab6e800f3172bdb))

Creates a pytest fixture for creating dataframes.

This uses a bit of magic. As pytest fixtures don't take arguments, we have it return a callable that
  does.

- **unit**: Add tests for get_unique_level and not_zero
  ([`1f99bc2`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1f99bc231554260e83793c6c63c84efe6d417052))

Adds unit tests for some of the data handling functions.

Currently, the tests only check that the return type is bool for not_zeros. This is better than
  nothing, but it still doesn't check whether the threshold works correctly. This will be setup in a
  coming release.


## v0.6.0 (2021-08-17)

### Code Style

- **typing**: Assert floats
  ([`a1d1ada`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a1d1ada9cc42bc7a9e0c63cc8bc54d98e591e71b))

In helpers.jaccard, an assert is used to tell mypy that yes, this optional float will in fact be a
  float.

### Documentation

- **README**: Expand usage instructions
  ([`173be97`](https://github.com/IMS-Bio2Core-Facility/lta/commit/173be9708feb9e41a89b2d77bd0c40357ccfa4f1))

The README now provides full installation and usage instructions for the CLI.

### Features

- **pipeline**: Calculate b_lipids
  ([`c11e563`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c11e563fb41d0caefa6b0a8fe0dcfbe7167ece0c))

The pipeline now calculates b-lipids, defined as any lipid present in any pair of tissues.


## v0.5.0 (2021-08-16)

### Documentation

- **help-messages**: Expand help messages
  ([`4dbd97f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4dbd97f50f32497017a40b0bb22c13c352c11822))

All options now have help messages.

### Features

- **pipeline**: Calculate jaccard for U-lipids
  ([`d43f0a4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d43f0a4a9d2f6e0e65445d8487f3ee65105664be))

Calculates the Jaccard distances for U-lipids. This required a slight tweak to the input of the
  calculation to accomodate the structure of B-lipids.

- **pipeline**: Identify U-lipids
  ([`03ef483`](https://github.com/IMS-Bio2Core-Facility/lta/commit/03ef4838497f59f97a290b6827814604f6d34719))

Adds support for identifying U-lipids - those lipids that are unique to a single tissue.

The code is not as concise as for A-lipids since the logic required to filter and split by tissue is
  more complex.

### Refactoring

- **pipeline**: Read data once
  ([`e5fbd4f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e5fbd4fe8a1a6fabdd5b98b63935df0aacf9ef7b))

The existing code was already assuming certain things about the structure of the input data. As
  such, using 2 data reads to create the index was unnecessary. By documenting the assumptions, the
  DF can be created in a single read.

- **pipeline**: Split data by mode
  ([`239fe44`](https://github.com/IMS-Bio2Core-Facility/lta/commit/239fe44d9fd79c2e9c488ff4422c3aa3d58e5a75))

The "split by mode" paradigm is also pervasive through out. Again, to prevent duplicates, the data
  is now split and stored at the post_init step.

- **pipeline**: Store boolean counts
  ([`517c8b3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/517c8b3186b3c51cccba185f606b3f1d12cfd9d7))

Nearly all analysis in the pipeline occurs on boolean counts. As such, to prevent duplicate
  calculations, the boolean values are calculated durint post_init for later retrieval.


## v0.4.0 (2021-08-13)

### Bug Fixes

- **command**: Add -b flag
  ([`8c1c645`](https://github.com/IMS-Bio2Core-Facility/lta/commit/8c1c6452465e1749fecd4d6fc1cb207dec5e0a04))

Adds a flag to specify the number of bootstrap repetitions to use.

- **jaccard**: Divide by abs(j_obs)
  ([`ca62ff9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ca62ff92a8f2c2483d7dd5c789dacd3490ed8ef4))

The p-value calculation is now correctly implemented.

- **jaccard**: Return when degenerate
  ([`78831b9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/78831b9b3342d8ffa681c93144d1012c6a48daa4))

When the bootstrap is degenerate, now return j and 1 (p_val) rather than raising a RuntimeError.

### Build System

- **deps**: Add numpy as dependency
  ([`8158068`](https://github.com/IMS-Bio2Core-Facility/lta/commit/81580689e68a6b25230a6778702249f58f56b25d))

Though it was already provided through Pandas, we now specify it as explicit.

- **nox**: Add xdoctest to pytest
  ([`d95d5c3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d95d5c37f3f8d51c4071a71e99f3e9ee2b8a5e5c))

### Continuous Integration

- **actions**: Remove doc_test action
  ([`94740b9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/94740b9f809d9cd88cf6ed86e28d9cb9da91708f))

- **tests**: Run xdoctest with pytest
  ([`5d6b3d3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5d6b3d32498aa2a4439ff19a320638dbfed18a6d))

Will minimise the number of installs, saving some time on CI builds.

### Documentation

- **jaccard**: Add docs to Sphinx
  ([`387637f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/387637f2a05c76e9ad4ca4dd2cef349d0c5003b4))

- **parser**: Add new opts to docstring
  ([`204ee65`](https://github.com/IMS-Bio2Core-Facility/lta/commit/204ee65ed042078a5c9cc2a09915b4fcc3946718))

### Features

- **jaccard**: Implement boolean Jaccard similarity
  ([`9b828bc`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9b828bcc0706efdb8d6a30fcc6ca812540ab6c4d))

Custom implementation of boolean Jaccard similarity. Citation given in module documentation.

- **pipeline**: Add jaccard calculations
  ([`f17f1e2`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f17f1e2cd1b27f08088651733c517dd346602988))

Adds a method for calculating Jaccard distanced and p-values to the pipeline, and enable it for
  a-lipids.

### Testing

- **unit**: Add tests for Jaccard
  ([`ee471a4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ee471a4c786ac1e18262c10b214eb532810ab6e2))

Provides unit tests for Jaccard module. Frequent use of numpy's assert_allclose to deal with
  floating points.


## v0.3.0 (2021-08-12)

### Bug Fixes

- **command**: Remove subscript of float
  ([`75c7cd6`](https://github.com/IMS-Bio2Core-Facility/lta/commit/75c7cd6a2a59f2b980bec6d276e5f8ce285918e4))

Since the type of thresh was specified as float in the parser, it is not necessary to subscript it
  when passed to the run command.

### Continuous Integration

- **dev-deps**: Add pytest-mock
  ([`c1e7452`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c1e74523700c43f1587e3d3ddd92662651e3cdd3))

Let's be real, this was always going to be necessary to handle the unit tests.

- **gitignore**: Ignore Makefile
  ([`f92ea97`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f92ea97231fd0f95709c3ec44c23030134f3f4d3))

Again, the Makefile is not necessary for either deployment or development, so ignore it.

### Documentation

- **pipeline**: Document new pipeline module
  ([`9b1c5a0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9b1c5a081202871d5e971b10e8eae2cd5347045a))

- **unit-tests**: Add docs for new pipeline tests
  ([`9994c70`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9994c70e44d75967e6d1dc52b850ef0a2bc28a54))

### Features

- **pipeline**: Introduce pipeline class
  ([`fc9a53e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/fc9a53e9b759bacf2c16caa0d4ce924080c1531e))

Introduces the pipeline dataclass. This class uses post_init to process the inputs, then runs the
  necessary steps to extract information about the various lipids through a unified, object oriented
  approach.

### Testing

- **unit/int**: Add tests for pipeline
  ([`2a0a2ac`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2a0a2acdb74598e62e131dba9c07baf21408f8f2))

Adds tests for error handling within the pipeline. Due to complexity, tests for data handling are
  forthcoming.

- **unit/int**: Mark data handling as xfail
  ([`8c24190`](https://github.com/IMS-Bio2Core-Facility/lta/commit/8c2419065ce60c685cd2b069e9b88ded700d3e40))

As previously commented, tests handling data processing will be forthcoming given the complexity of
  mocking that data. As such, those tests dependent on these features are now marked xfail.


## v0.2.0 (2021-08-11)

### Bug Fixes

- **simple**: Print threshold
  ([`6e86a3c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6e86a3c5989fb9735f139c542e14d0b9c3cd14cc))

Not sure why this wasn't committed earlier, but the simple command now also prints the threshold.

### Build System

- **deps**: Add pandas
  ([`82574cb`](https://github.com/IMS-Bio2Core-Facility/lta/commit/82574cbef679c8bb3d0c91a07df4d91079140ae3))

The in-built dataframe functionality of R more or less requires pandas if we don't want to re-write
  all CSV handlers manually.

- **gitignore**: Ignore data/results
  ([`7529af7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7529af77c0103aa7dccc9d380abc5e50cc0e3b20))

Again, hiding scratch work we don't want/need to commit.

- **gitignore**: Ignore scratch file
  ([`e80a35e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e80a35e6fe0354da362be659543869030b690cd1))

While translating from R, some test space is useful, but not necessary for the repo.

### Documentation

- **helpers**: Document new functionality
  ([`ae9c45b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ae9c45ba879a7c1065629976157b80e6ddca0105))

### Features

- **helpers**: Add FloatRange type
  ([`6db2b00`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6db2b00f1bfca9e1a5f5ecf059e47320a957d331))

A custom container that support float ranges. Principally, this lets us assert `choices` for
  argparser on a float argument.

- **parser**: Add threshold option
  ([`1b6dc0a`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1b6dc0a9c7a4eb6ef93477bc794f82be6d004269))

Adds a threshold option. Given nargs=1, it will provide a default if not specified, but a float must
  be given if the flag is passed.

- **parser**: Support specification of input and output files
  ([`e523fc0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e523fc0313815b974f7b20a4c05aaee9e47c6c04))

The parser now expects two positional arguments: data and output. Respectively, these indicate where
  the input data is, and where the output files will go.

Technically breaking, as it alters the CLI. But do not intend to increment major until we are
  stable.

### Testing

- **unit**: Test thresh option
  ([`57408a5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/57408a50fc0aa6adc654771b3af044e3d59a5980))

TDD: test usage of forthcoming threshold option.

- **unit/int**: Add tests for FloatRange
  ([`abf0d40`](https://github.com/IMS-Bio2Core-Facility/lta/commit/abf0d405af40ab7aa907d290278403f78a5a155d))

TDD: adds tests for the FloatRange option.

- **Unit/Int**: Support new arg structure
  ([`f538310`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f53831013dbc1280f1edd2aa9951b31ce250f308))

TDD: adds tests for the new argument structure of the parser and CLI.


## v0.1.0 (2021-08-06)

### Continuous Integration

- **actions**: Matrix across OS
  ([`247929e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/247929e775288714e7f23c7afb11e04f683bfebe))

Runs all tests across Ubuntu, MacOS, and Windows. Coverage is tagged and uploaded appropriately.
  Additionally, release is on run on Ubuntu.

- **actions**: Migrate to codecov-action v2
  ([`86ab150`](https://github.com/IMS-Bio2Core-Facility/lta/commit/86ab150e05186a95acef5427632ac80a87ea49ce))

- **actions**: Reduce matrix
  ([`7d2a48b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7d2a48b5c36e1a58a30897c69415fab732008d90))

After some initial fun, the reality is that only the test suite might reveal OS-dependent bugs. The
  Safety-DB is OS-independent, as is formatting and linting. Additionally, the Safety-DB is python
  version independent.

- **actions**: Use OS-independent files
  ([`d11b844`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d11b8449cb293e881355e46b916b8b6032eede91))

tempfile.NamedTempFile currently has issues with being used in a context manager on Windows. To
  avoid this issue, we directly name and remove the file using the OS-independent os module.

### Documentation

- **README**: Add badges to documentation
  ([`bc7f42d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bc7f42d37c962350eb64d699afb69595a72d6d02))

### Features

- **repo**: Initialise repository
  ([`403d523`](https://github.com/IMS-Bio2Core-Facility/lta/commit/403d523db23739041cb2d3769cc17746210c1a41))

Initialises the repository, providing a minimal functional framework on which to build the tool.
