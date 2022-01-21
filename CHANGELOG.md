# Changelog

<!--next-version-placeholder-->

## v2.0.0 (2022-01-21)
### Feature
* **examples:** Provide minimum working examples ([`c0575f8`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c0575f8eb3f4825c0e691acfc8b431e4e9a015e2))
* **cli:** Calculate enfc against control ([`f9d7e6b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f9d7e6b7f2548a2afbe2ab2a894fc88134c3935d))

### Fix
* **parser.py:** Update default parameters ([`878df07`](https://github.com/IMS-Bio2Core-Facility/lta/commit/878df07b5df494c2a95d6f479737b973b66d4a4b))

### Breaking
* Current users should update any scripts and configs to use the new `--compartment` flag rather than the existing `--tissue` flag.  ([`5ca9aed`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5ca9aed96cc692226edde90f75a33a3f1e22daef))
* Users should update their configuration files to ensure that they specify 0.2 as the threshold if they wish to continue using the old value.  ([`878df07`](https://github.com/IMS-Bio2Core-Facility/lta/commit/878df07b5df494c2a95d6f479737b973b66d4a4b))
* Previously, if multiple fold change calculations were desired, the user had to call `lta` multiple times. Now, a single call produces all fold change calculations for a set of experimental conditions. This feature could have been implemented by having the user specify all pairs they were interested in. While this could introduce more flexibility (ie it would allow for multiple "controls"), it also introduces more overhead for both the user and maintainer. Additionally, for the vast majority of experimental designs, there will be only one control. Closes #17.  ([`f9d7e6b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f9d7e6b7f2548a2afbe2ab2a894fc88134c3935d))

### Documentation
* **README.md:** Enumerate defaults ([`3404845`](https://github.com/IMS-Bio2Core-Facility/lta/commit/34048454bd116bf521ce8c02e45a50133b3851b8))
* **pipeline.py:** Update docstrings for new functions ([`35e98d0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/35e98d0387bfab0e6b7b59959ce451b2f51682ac))
* **LICENSE:** Update copyright year ([`d4fd7a0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d4fd7a0e54743c1056e6b8e8b9ea41eb75c3a579))
* **README.md:** Update usage instructions ([`cdc2f09`](https://github.com/IMS-Bio2Core-Facility/lta/commit/cdc2f09ac306a299f5c27189bff25fb7f045f598))
* **README.md:** Add python installation instructions ([`4fc9b83`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4fc9b83a67443349e254237d03e84f2dbd731d8f))

## v1.0.0 (2022-01-07)
### Feature
* **cli:** Change phenotype to group ([`6b91841`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6b918419e88136e2a47edccb65a0ff31cbace70e))
* **cli:** Generalise data reading ([`d5ce9f5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d5ce9f594ff3380ab4cc6cd77fd3f64113530173))

### Breaking
* Change "phenotype" to "group". Existing users will need to make sure that any scripts and config files use this new flag.  ([`6b91841`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6b918419e88136e2a47edccb65a0ff31cbace70e))
* This introduces 2 new command line flags and changes how the data is processed. Past scripts are not guaranteed to run correctly - unless, by chance, they used the defaults - so a breaking release is required.  ([`d5ce9f5`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d5ce9f594ff3380ab4cc6cd77fd3f64113530173))

### Documentation
* **README.md:** Update usage for new flags ([`75772f7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/75772f7b81f6bf518b9e5cc55656b5a0740f5dda))

## v0.12.5 (2022-01-04)
### Fix
* **lta.py:** Remove colons from filenames ([`3e4388c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3e4388cfcc5c906ac384195c17588dd6edd0a53f))

## v0.12.4 (2022-01-04)
### Fix
* **pipeline.py:** Respect metadata locations ([`e906e87`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e906e87816305e071fc47fe6189b817095b08959))

### Documentation
* **repo:** Use Traffic throughout ([`af3c4d1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/af3c4d1554215251b8a4432db3b8a1aba4d1a1e7))
* **README.md:** Update badges ([`57718d4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/57718d41d7a1b49e70ec9fb58c0f32b76b8ea9e2))

## v0.12.3 (2021-12-23)
### Fix
* **pyproject.toml:** Correct version number ([`0b01aea`](https://github.com/IMS-Bio2Core-Facility/lta/commit/0b01aea41f8cab8a61f4d2d1b85cd864f04bb656))
* **pyproject.toml:** Correct included packages ([`d603a6c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d603a6c904c494b480e2b5daa14b1fc267ab1cec))

## v0.12.2 (2021-12-23)
### Fix
* **repo:** Support python3.10 ([`0edba28`](https://github.com/IMS-Bio2Core-Facility/lta/commit/0edba28f5bf7291379aa4f59b9faee279f5ae39b))

### Documentation
* **docs/index.md:** Correct badges ([`1f3685e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1f3685ea9056496c09f62a62b99d177a337d20c2))
* **README:** Add links ([`f26fe30`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f26fe3005b35541c6cf36b5ca880b98239f7f688))
* **readthedocs:** Specify build dependencies ([`61837c3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/61837c33f902d89c2b0d7d35ef23a5635e67d743))
* **README:** Update project name and status ([`85e235c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/85e235cbf8f70accf2041cf9d6ecc1c675cd4414))
* **README:** Add future work ([`1304204`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1304204d6de27b7c2fe05fd34d27fc53ccb71751))

## v0.12.1 (2021-09-16)
### Fix
* **data_handling:** Report senseless FC as 0 ([`1e0ae79`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1e0ae79ef81452441f1b7bfb1c3f606364694d99))

### Documentation
* **README:** Document NaN's in output ([`4ebc261`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4ebc2613cea1e47f2d16568d6a427f433a8f7c1c))

## v0.12.0 (2021-09-16)
### Feature
* **logging:** Add logfile option ([`2d0bd60`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2d0bd60ce3cf619a39a4b4c6c6821b7576ca470a))
* **logging:** Introduce logging support ([`431822a`](https://github.com/IMS-Bio2Core-Facility/lta/commit/431822a1136a25483c799a21d841c6ae3fe96a21))

### Fix
* **pipeline:** Change output file names ([`3b9bdbe`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3b9bdbe9c6a2a2df798f5522ac5e5ab483af1ed6))
* **pipeline:** Calculate Jaccard similarity ([`4b21ade`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4b21adea2dfc9b4fabe20bff646b2ef1b9bd0cb7))
* **logging:** Correct use of logger ([`9b332b3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9b332b3579a32a62a7e1ccc994a5705d9c430d36))
* **logging:** Respect verbosity flag ([`5373dd2`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5373dd2447e2cad2b749448de4242632c2ba824f))
* **logging:** Add logging for data_handling ([`73a2aa3`](https://github.com/IMS-Bio2Core-Facility/lta/commit/73a2aa3329b30998c4c16ac9b738b31e87d21085))
* **logging:** Add logging for Jaccard ([`a35e851`](https://github.com/IMS-Bio2Core-Facility/lta/commit/a35e8519f036a0911ce789467494cef7f7ee8a45))
* **logging:** Add logging to pipeline ([`3af0c53`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3af0c5368877689a655ce2919c2b42ad01496c6f))

### Documentation
* **README:** Update file name output ([`3e2c1df`](https://github.com/IMS-Bio2Core-Facility/lta/commit/3e2c1df3af86fd9d00a10721d263e05fce05a68e))

## v0.11.1 (2021-08-26)
### Fix
* **data_handling:** Respect axis in enfc ([`2d727f7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2d727f716c06e972e4228f2932f572d5ed16b015))

## v0.11.0 (2021-08-26)
### Feature
* **pipeline:** Support summary enfc ([`e927354`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e927354caf4709f9a65eb1a5bb22b10ea90bcfda))
* **pipeline:** Summary jaccard output ([`742dde1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/742dde161ad9c25926faafe56d66e5ef9c85d6b1))
* **pipeline:** Output summary files ([`2e51efd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2e51efde9e30c7ffc66b236c847ea0a77951b935))

### Documentation
* **pipeline:** Document summary files ([`700c8fb`](https://github.com/IMS-Bio2Core-Facility/lta/commit/700c8fbb63e45d2dc4fb465f179d840652bef419))

## v0.10.1 (2021-08-25)
### Fix
* **repo:** Fix build failures ([`9ced474`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9ced474825e59ae8cbacc20957917be16913b60d))

### Documentation
* **conftest:** Add conftest to sphinx ([`e2d9174`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e2d9174664c77d0cd946fdde5dc9660981d00c9e))
* **README:** Reflect unified input file usage ([`c7b18e9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c7b18e906f5087a605326fd031caf0e598c5c652))
* **command:** Document unified input ([`58592ce`](https://github.com/IMS-Bio2Core-Facility/lta/commit/58592ce4ba844409030619c531aee7ed0500dae1))
* **helpers:** Update docs to unified input ([`f94996c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f94996cbf937649df8cb6517fbc36de9e36d6f57))

## v0.10.0 (2021-08-20)
### Feature
* **pipeline:** Calculate enfc ([`05ecf05`](https://github.com/IMS-Bio2Core-Facility/lta/commit/05ecf05fe6ab3264ed110950eb97055ccba23b70))
* **data_handling:** Calculate enfc ([`e7c28af`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e7c28af36730b913ef8fb648e9087256fefe19a9))

### Fix
* **parser:** Reduce boot-reps ([`5e339fb`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5e339fbcef5971e14f27823509439fac4d59fe94))
* **parser:** Do not specify nargs ([`41ec8fd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/41ec8fda00037fd2e99a5df74ad0805bc7ff8aaf))
* **command:** Order is now user option ([`7aa7413`](https://github.com/IMS-Bio2Core-Facility/lta/commit/7aa741393a394bca56699b8e1cede06d1401266c))

### Documentation
* **enfc:** Add support documentation ([`c1eb26e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c1eb26ed22e53a163e9755f44de4aec41c32d48b))

## v0.9.0 (2021-08-19)
### Feature
* **parser:** Add phenotype and tissue flags ([`2acbcc7`](https://github.com/IMS-Bio2Core-Facility/lta/commit/2acbcc76fd8ed868304fd3c53afc52dff00a5e45))

### Documentation
* **data_handling:** Add docs for data-handling ([`5a52bd0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/5a52bd0c8445b0b58330c977dac7e39a021cba8a))
* **README:** Document all options ([`8c8ee48`](https://github.com/IMS-Bio2Core-Facility/lta/commit/8c8ee48e1733d2618631e425a1013029021fb3dd))
* **README:** Document output of analysis ([`17a02e8`](https://github.com/IMS-Bio2Core-Facility/lta/commit/17a02e814c4b848b7de07612507c25dfa7825048))
* **README:** Document config file ([`b05f8c9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/b05f8c9325eeedba3c78771eb0fe293e575c78e6))

## v0.8.0 (2021-08-19)
### Feature
* **pipeline:** Support N-lipids ([`9f0abbb`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9f0abbbc4e905f521a60e8b65dbe4dcc1e7a7d18))

### Fix
* **pipeline:** Capitalise tissue names ([`06294fd`](https://github.com/IMS-Bio2Core-Facility/lta/commit/06294fdbd6e4b37827e30445d7698c2c676d585b))

## v0.7.0 (2021-08-18)
### Feature
* **pipeline:** Split b-lipids ([`9254797`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9254797220ee78147081c00129024e6da34d3f15))

## v0.6.1 (2021-08-18)
### Fix
* **unit_tests:** Use binary_df fixture ([`46875fa`](https://github.com/IMS-Bio2Core-Facility/lta/commit/46875fa9ced48594012a3b8ef3831786e3d2c68c))
* **data_handling:** Correct column/index check ([`bf143f1`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bf143f1bf6f978e59459a35d984e84735b5bd769))
* **pipeline:** Generalise _split_data level ([`9fb0c7e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9fb0c7e12393cc00dff0f17896adb5ca7ca97f3f))

## v0.6.0 (2021-08-17)
### Feature
* **pipeline:** Calculate b_lipids ([`c11e563`](https://github.com/IMS-Bio2Core-Facility/lta/commit/c11e563fb41d0caefa6b0a8fe0dcfbe7167ece0c))

### Documentation
* **README:** Expand usage instructions ([`173be97`](https://github.com/IMS-Bio2Core-Facility/lta/commit/173be9708feb9e41a89b2d77bd0c40357ccfa4f1))

## v0.5.0 (2021-08-16)
### Feature
* **pipeline:** Calculate jaccard for U-lipids ([`d43f0a4`](https://github.com/IMS-Bio2Core-Facility/lta/commit/d43f0a4a9d2f6e0e65445d8487f3ee65105664be))
* **pipeline:** Identify U-lipids ([`03ef483`](https://github.com/IMS-Bio2Core-Facility/lta/commit/03ef4838497f59f97a290b6827814604f6d34719))

### Documentation
* **help-messages:** Expand help messages ([`4dbd97f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/4dbd97f50f32497017a40b0bb22c13c352c11822))

## v0.4.0 (2021-08-13)
### Feature
* **pipeline:** Add jaccard calculations ([`f17f1e2`](https://github.com/IMS-Bio2Core-Facility/lta/commit/f17f1e2cd1b27f08088651733c517dd346602988))
* **jaccard:** Implement boolean Jaccard similarity ([`9b828bc`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9b828bcc0706efdb8d6a30fcc6ca812540ab6c4d))

### Fix
* **command:** Add -b flag ([`8c1c645`](https://github.com/IMS-Bio2Core-Facility/lta/commit/8c1c6452465e1749fecd4d6fc1cb207dec5e0a04))
* **jaccard:** Divide by abs(j_obs) ([`ca62ff9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ca62ff92a8f2c2483d7dd5c789dacd3490ed8ef4))
* **jaccard:** Return when degenerate ([`78831b9`](https://github.com/IMS-Bio2Core-Facility/lta/commit/78831b9b3342d8ffa681c93144d1012c6a48daa4))

### Documentation
* **parser:** Add new opts to docstring ([`204ee65`](https://github.com/IMS-Bio2Core-Facility/lta/commit/204ee65ed042078a5c9cc2a09915b4fcc3946718))
* **jaccard:** Add docs to Sphinx ([`387637f`](https://github.com/IMS-Bio2Core-Facility/lta/commit/387637f2a05c76e9ad4ca4dd2cef349d0c5003b4))

## v0.3.0 (2021-08-12)
### Feature
* **pipeline:** Introduce pipeline class ([`fc9a53e`](https://github.com/IMS-Bio2Core-Facility/lta/commit/fc9a53e9b759bacf2c16caa0d4ce924080c1531e))

### Fix
* **command:** Remove subscript of float ([`75c7cd6`](https://github.com/IMS-Bio2Core-Facility/lta/commit/75c7cd6a2a59f2b980bec6d276e5f8ce285918e4))

### Documentation
* **unit-tests:** Add docs for new pipeline tests ([`9994c70`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9994c70e44d75967e6d1dc52b850ef0a2bc28a54))
* **pipeline:** Document new pipeline module ([`9b1c5a0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/9b1c5a081202871d5e971b10e8eae2cd5347045a))

## v0.2.0 (2021-08-11)
### Feature
* **helpers:** Add FloatRange type ([`6db2b00`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6db2b00f1bfca9e1a5f5ecf059e47320a957d331))
* **parser:** Add threshold option ([`1b6dc0a`](https://github.com/IMS-Bio2Core-Facility/lta/commit/1b6dc0a9c7a4eb6ef93477bc794f82be6d004269))
* **parser:** Support specification of input and output files ([`e523fc0`](https://github.com/IMS-Bio2Core-Facility/lta/commit/e523fc0313815b974f7b20a4c05aaee9e47c6c04))

### Fix
* **simple:** Print threshold ([`6e86a3c`](https://github.com/IMS-Bio2Core-Facility/lta/commit/6e86a3c5989fb9735f139c542e14d0b9c3cd14cc))

### Documentation
* **helpers:** Document new functionality ([`ae9c45b`](https://github.com/IMS-Bio2Core-Facility/lta/commit/ae9c45ba879a7c1065629976157b80e6ddca0105))
* **README:** Add badges to documentation ([`bc7f42d`](https://github.com/IMS-Bio2Core-Facility/lta/commit/bc7f42d37c962350eb64d699afb69595a72d6d02))

## v0.1.0 (2021-08-06)
### Feature
* **repo:** Initialise repository ([`403d523`](https://github.com/IMS-Bio2Core-Facility/lta/commit/403d523db23739041cb2d3769cc17746210c1a41))
