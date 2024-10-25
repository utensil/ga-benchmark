prep-bench:
  #!/usr/bin/env bash
  brew install cairomm pangomm
  brew link cairomm --force
  brew link pangomm --force
  xrepo install benchmark
  xrepo env -y xmake build bench

@find NAME:
    xmake require -v --search {{NAME}} || true
    xmake require -v --search "vcpkg::{{NAME}}" || true
    xmake require -v --search "conan::{{NAME}}" || true
    # xmake require -v --search "conda::{{NAME}}" || true
    xmake require -v --search "cmake::{{NAME}}" || true
    # xmake require --search "clib::{{NAME}}" || true
    xmake require --search "brew::{{NAME}}" || true

@info NAME:
    xmake require --info {{NAME}}

@fetch NAME:
    xmake require --fetch {{NAME}}

@list:
    xmake require --list
