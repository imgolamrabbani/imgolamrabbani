<div align="center">

# MD Golam Rabbani (`@imgolamrabbani`). 

**Security Researcher · Systems Bug Hunter · Open-Source Contributor**

[Auto-Sync](https://www.google.com/search?q=https://github.com/imgolamrabbani/imgolamrabbani/actions/workflows/update-readme.yml)

</div>

> Auditing systems code, hunting memory-safety and access-control vulnerabilities, and shipping upstream patches to open-source infrastructure. Everything below is **automatically synced via GitHub Actions** (`update-readme.yml`) from live GitHub APIs.

## 🚨 Security Advisories & CVE Disclosures (GHSA / CVE)

<!-- AUTO-ADVISORIES:START -->

* [**InvoicePlane/InvoicePlane · GHSA-2849-wpq6-pq9g**](https://github.com/InvoicePlane/InvoicePlane/security/advisories/GHSA-2849-wpq6-pq9g#event-1234159)   `CWE-284 / CWE-200` — Unauthenticated direct route access to `Payment_information::stripe()` and `paypal()` disclosed gateway public key / client ID and settings even with online payments disabled *(Patched in [#1837](https://github.com/InvoicePlane/InvoicePlane/pull/1837), [#1838](https://github.com/InvoicePlane/InvoicePlane/pull/1838) · [Changelog Credit](https://github.com/InvoicePlane/InvoicePlane/blob/develop/.github/CHANGELOG.md))*

* [**InvoicePlane/InvoicePlane · GHSA-ppgp-rvmx-2wp5**](https://github.com/InvoicePlane/InvoicePlane/security/advisories/GHSA-ppgp-rvmx-2wp5#event-1234161)   `CWE-639 / CWE-862` — Client assignments of any user readable by a secondary administrator via `users/ajax/load_user_client_table`, `users/ajax/modal_add_user_client`, and `user_clients/user/<id>` *(Patched in [#1836](https://github.com/InvoicePlane/InvoicePlane/pull/1836) · [Changelog Credit](https://github.com/InvoicePlane/InvoicePlane/blob/develop/.github/CHANGELOG.md))* <!-- AUTO-ADVISORIES:END -->

## 🔧 Open-Source Pull Requests & Security Patches

<!-- AUTO-PRS:START -->

* [**microsoft/msquic#6418**](https://github.com/microsoft/msquic/pull/6418)   — Fix `DestCid` lifecycle edge cases in `QuicPathRemove` and `QuicPathUpdateDestCids` (`#6416`)

* [**Abdullah-Ash-Shafi/Inventory-Management-System#2**](https://github.com/Abdullah-Ash-Shafi/Inventory-Management-System/pull/2)   — `feat(darkstore)`: add proximity checks and threshold replenishment strategy

* [**Abdullah-Ash-Shafi/SE_Git_Snake#4**](https://github.com/Abdullah-Ash-Shafi/SE_Git_Snake/pull/4)   — Add snake game styling and rendering

<details open> <summary><strong>ggml-org/ggml</strong> – 2 PRs <img alt="stars" src="https://img.shields.io/github/stars/ggml-org/ggml?style=flat-square&label=stars&color=DAA520"></summary>

* [**ggml-org/ggml#1673**](https://github.com/ggml-org/ggml/pull/1673)  — `gguf`: fix tensor shape overflow check mismatch and add regression test (`#1668`)

* [**ggml-org/ggml#1671**](https://github.com/ggml-org/ggml/pull/1671)  — `ggml-rpc` : fix tensor bounds checks, `recv_msg` `length_error`, and destructor synchronization

</details>

<details open>
<summary><strong>monicahq/monica</strong> – 3 PRs <img alt="stars" src="https://img.shields.io/github/stars/monicahq/monica?style=flat-square&label=stars&color=DAA520"></summary>

* [**monicahq/monica#7983**](https://github.com/monicahq/monica/pull/7983)  — `fix`: use correct `sliceOfLife-owner` gate in web routes

* [**monicahq/monica#7982**](https://github.com/monicahq/monica/pull/7982)  — `fix`: scope contact reminder deletion to target vault in `RemoveVaultAccess`

* [**monicahq/monica#7981**](https://github.com/monicahq/monica/pull/7981)  — `fix`: enforce write token ability on `VaultController::destroy`

</details>

<details>
<summary><strong>Songram-Biswas/CSE-3206</strong> – 2 PRs <img alt="stars" src="https://img.shields.io/github/stars/Songram-Biswas/CSE-3206?style=flat-square&label=stars&color=DAA520"></summary>

* [**Songram-Biswas/CSE-3206#3**](https://github.com/Songram-Biswas/CSE-3206/pull/3)  — Add editing note to README

* [**Songram-Biswas/CSE-3206#2**](https://github.com/Songram-Biswas/CSE-3206/pull/2)  — Add initial content to README.md

</details>
<!-- AUTO-PRS:END -->

## 🛡️ Vulnerability Research & Upstream Bug Reports

<!-- AUTO-ISSUES:START -->

* [**bellard/quickjs#576**](https://github.com/bellard/quickjs/issues/576)   — NULL dereference in `JS_ReadObjectRec` on TypedArray self-reference

* [**microsoft/msquic#6416**](https://github.com/microsoft/msquic/issues/6416)   — `path`: `DestCid` lifecycle edge cases in `QuicPathRemove` and `QuicPathUpdateDestCids`

* [**ggml-org/ggml#1670**](https://github.com/ggml-org/ggml/issues/1670)   — `ggml-rpc`: fix bounds checks on 0-element tensors / offset wrap-around, uncaught `length_error` in `recv_msg`, and missing sync in `~rpc_server`

* [**ggml-org/ggml#1668**](https://github.com/ggml-org/ggml/issues/1668)   — `gguf`: tensor shape overflow check mismatch between `gguf_init_from_reader` and `ggml_new_tensor_impl`
  <!-- AUTO-ISSUES:END -->

## ⚡ Selected Personal Projects

| Project | Stack | Description | 
| ----- | ----- | ----- | 
| [**SpeedMeter**](https://www.google.com/search?q=https://github.com/imgolamrabbani/SpeedMeter) | `Swift` · `macOS` | Native macOS menu bar utility for real-time network throughput monitoring and bandwidth usage tracking. | 
| [**CyberAcademy**](https://www.google.com/search?q=https://github.com/imgolamrabbani/CyberAcademy) | `HTML` · `Python` · `Docker` | Interactive cybersecurity learning platform with hands-on labs, CTF challenges, and guided security tracks. | 
| [**NutrientScann**](https://www.google.com/search?q=https://github.com/imgolamrabbani/NutrientScann) | `Python` · `JavaScript` · `AI` | Smart nutrition scanner that analyzes food items to provide nutritional breakdowns and health insights. | 
| [**ExamSQL**](https://www.google.com/search?q=https://github.com/imgolamrabbani/ExamSQL) / [**SQLMAX**](https://www.google.com/search?q=https://github.com/imgolamrabbani/SQLMAX) | `JavaScript` · `SQL` | Interactive SQL practice, query evaluation, and database management utilities. | 
| [**cloudshell-tunnel**](https://www.google.com/search?q=https://github.com/imgolamrabbani/cloudshell-tunnel) | `Shell` · `Linux` | Lightweight automation scripts for establishing and managing secure remote shell tunnels. | 

## 🧰 Technical Arsenal

* **Security & Auditing:** Vulnerability Research, Source Code Auditing, Memory Safety (ASan/UBSan/Fuzzing), Burp Suite, Wireshark, Nmap, Metasploit, OWASP Top 10, Kali / Parrot OS

* **Languages & Runtimes:** C / C++, Python, JavaScript / TypeScript, Swift, PHP, SQL, Bash

* **Systems & Infrastructure:** Linux Internals, QUIC / TCP-IP Networking, Docker, Git, Node.js, React
