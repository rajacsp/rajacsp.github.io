Title: macOS System Info Commands You Should Know
Date: 2026-05-01
Category: DevTools
Tags: macos, terminal, cli, sysadmin, commands
Slug: macos-system-info-commands

Getting your macOS system and disk information from the terminal is straightforward once you know the right commands. Here's a quick reference.

## System Info

**`system_profiler SPSoftwareDataType`** — Displays macOS version, build number, kernel version, boot volume, and uptime. Good for confirming your OS details quickly.

Use like this in your terminal:

```bash
system_profiler SPSoftwareDataType
```

## Hardware Overview

**`system_profiler SPHardwareDataType`** — Shows CPU model, core count, memory (RAM), serial number, and hardware UUID. Essential when you need machine specs.

Use like this in your terminal:

```bash
system_profiler SPHardwareDataType
```

## Disk Info

**`diskutil list`** — Lists all disks and partitions with their identifiers (e.g., disk0, disk1). Useful for understanding your disk layout before any partition or format work.

Use like this in your terminal:

```bash
diskutil list
```

## Disk Usage

**`df -h`** — Prints human-readable disk usage per mounted volume. The `-h` flag converts bytes into KB/MB/GB for easy reading.

Use like this in your terminal:

```bash
df -h
```

## Storage Deep Dive

**`system_profiler SPStorageDataType`** — Goes beyond `df -h` by showing volume type, file system format, SMART status, and physical disk details.

Use like this in your terminal:

```bash
system_profiler SPStorageDataType
```

## All-in-One Summary

**`system_profiler SPSoftwareDataType SPHardwareDataType SPStorageDataType`** — Runs all three profiler modules in one shot. Best when you need a full snapshot for documentation or bug reports.

Use like this in your terminal:

```bash
system_profiler SPSoftwareDataType SPHardwareDataType SPStorageDataType
```

## Quick One-Liner

**`sw_vers && system_profiler SPHardwareDataType && df -h`** — The most popular combo. `sw_vers` gives a compact OS version block, followed by hardware and disk usage. Fast and readable.

Use like this in your terminal:

```bash
sw_vers && system_profiler SPHardwareDataType && df -h
```

---

Running `system_profiler` without any flags dumps everything, but expect it to take a minute or two. For daily use, the one-liner or individual flags are the way to go.