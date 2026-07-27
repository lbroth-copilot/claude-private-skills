# The four comment types

Contents:
1. status
2. analysis
3. handover
4. decision
5. Choosing when several fit

Each type has a shape and a worked example. The shape is an ordering of information, not a
template to fill in. Do not print the field names as bold labels in the comment.

---

## 1. status

Shape:
1. State right now (done / blocked / in progress on what exactly)
2. Evidence, one link or one command output
3. What is next and who does it

Length: 2-5 lines. Nobody reads a long status update.

Example:

> Build for `cf-nginx:1.29.1` is through and pushed to Harbor. Trivy scan is clean except
> CVE-2026-3021 in `libxml2`, which Ubuntu has not fixed yet, so I left it open for now.
> Next step is the deploy PR against `if-deployment-center`, I will open it tomorrow
> morning unless someone needs it earlier.

Blocked variant. Say what unblocks it, otherwise the comment is just a complaint:

> Stuck on the submodule update. `git submodule update --remote` pulls tag v3.2.0 but the
> workflow pins v3.1.4 through `versions.txt`, and I do not know which one is intended.
> @andreas, which version should the 24.04 image ship? I will keep the branch as-is until
> then.

## 2. analysis

Shape:
1. The conclusion, first sentence
2. How you got there, with the evidence a reader could reproduce
3. What follows from it
4. What you did not check

Putting the conclusion first is the biggest single readability win. A junior reading a
chronological investigation has to hold everything in their head before it pays off.

Example:

> The container crashes because the entrypoint runs as UID 1000 but `/var/lib/redis` is
> owned by root in the base layer.
>
> I reproduced it with:
>
> ```
> docker run --rm -u 1000 cf-redis:8.4.0 redis-server /etc/redis/redis.conf
> # Fatal error, can't open the append-only file: Permission denied
> ```
>
> The `chown` in our Dockerfile sits before the `COPY` of the config, so the copy resets
> the directory owner. Moving the `chown` to the last layer fixes it locally.
>
> I have not checked whether the same ordering problem exists in cf-valkey. It uses the
> same base, so it probably does.

## 3. handover

Shape:
1. Where things stand in one sentence
2. Numbered steps to continue, each one runnable
3. How to tell it worked
4. Where the traps are

This is the type where the junior-dev level matters most. Write the step you would skip
because it is obvious, because it is only obvious to you.

Example:

> Branch `fix/if-1288-size-metric` has the patch, it is not merged yet. To finish it:
>
> 1. `gh pr checkout 42` in `~/projects/cf-alloy`
> 2. Rebuild locally: `make build VERSION=1.6.1`
> 3. Check the size the way the test does, `docker export <id> | wc -c`, not
>    `docker inspect --format '{{.Size}}'`. The inspect value counts layers differently and
>    that is exactly the flake we are fixing.
> 4. Expected result is under 190 MB. I got 187.3 MB.
>
> One trap: the CI runner caches the base image, so a red pipeline right after a base image
> bump often means a stale cache and not your change. Re-run the job once before digging in.

## 4. decision

Shape:
1. What was decided
2. The one reason that actually drove it
3. What was rejected, and the specific cost that killed it
4. When the decision should be revisited

Do not present a balanced pro/con table. Name the deciding factor.

Example:

> We are going with a VEX statement for CVE-2026-4410 instead of backporting the fix.
>
> The backport was the first choice, but the upstream patch touches the vendored copy of
> `libssh2` and our build applies four patches to that same file already. Rebasing them
> took two hours and still broke the FIPS build, so the cost is out of proportion to a
> finding that is not reachable from any running process.
>
> Revisit this when we move to the 2.0 branch, which drops the vendored copy. Then the
> backport becomes a version bump.

Review outcome variant:

> Approved with one change requested. The retry loop in `pkg/fetch/client.go:88` has no
> upper bound, so a permanently failing registry keeps the job alive until the runner
> timeout at six hours. Cap it at five attempts with a backoff, then everything else looks
> fine to me.

## 5. Choosing when several fit

An investigation that ends in a choice is a `decision`, not an `analysis`. Lead with the
choice.

An analysis someone else has to continue is a `handover`. The steps matter more than the
reasoning, so put the steps first and compress the reasoning to two lines.

When the user really needs two things said, write two comments. One comment carries one
message.
