#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * setuid program that adds its process uid to /etc/passwd (if not already there)
 *
 * This is a workaround to OpenSSH client refusing to work when current uid is
 * not found in /etc/passwd:
 *    https://potyarkin.ml/posts/2022/no-user-exists-for-uid/
 *    https://superuser.com/questions/1704482/run-ssh-as-a-non-existent-virtual-user
 */
int main() {
    struct passwd* pw_entry;
    uid_t uid = getuid();
    pw_entry = getpwuid(uid);

    /* Exit early if current uid is already in /etc/passwd */
    if (pw_entry) {
        exit(0);
    }

    /* Add current uid:gid to /etc/passwd */
    gid_t gid = getgid();
    printf("Creating /etc/passwd entry for %d:%d\n", uid, gid);
    FILE* etc_passwd;
    etc_passwd = fopen("/etc/passwd", "a");
    fprintf(
        etc_passwd,
        "random_uid_%d:!:%d:%d::/nonexistent:/usr/sbin/nologin\n",
        uid, uid, gid
    );
    fclose(etc_passwd);
}
