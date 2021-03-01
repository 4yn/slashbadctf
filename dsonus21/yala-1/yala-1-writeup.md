# YALA (Part 1)

> Time to look at Yet Another Login App.  
> Try to find the right credentials and login!
> 
> Files (Any of the links are fine):  
> https://nusdsoctf2.s3-ap-southeast-1.amazonaws.com/S3/YALA/login2.apk  
> https://nusdsoctf.s3-ap-southeast-1.amazonaws.com/S3/YALA/login2.apk  
> [Attachment: login2.apk](./challenge/login2.apk)

Writeup by [@4yn](https://github.com/4yn)

Extract `classes.dex` and inspect with jadx.

```bash
$ unzip -j challenge/login2.apk classes.dex -d .
Archive:  challenge/login2.apk
  inflating: ./classes.dex
```

Inspect with jadx.

```java
// com.ctf.level3.data.LoginDataSource
public class LoginDataSource {
    /* renamed from: c  reason: collision with root package name */
    public final byte[] f1391c = c.a("516b36ed915a70852daf6a06c7fd1a1451d8269a8b2c5ae97110bc77b083c420");
}
```

Looks like some encrypted flag or a hash. Find usage brings to another package.

```java
// b.b.a.e.a.d
public class d extends p {
    public void b(String str, String str2) {
        Object obj;
        LoginDataSource loginDataSource = this.f1112d.f1100a;
        Objects.requireNonNull(loginDataSource);
        String aVar = new a(loginDataSource).toString(); // Username get
        loginDataSource.f1392d = aVar;
        if (!str.equals(aVar)) { // Username check
            Log.d("ctflevel2", "Invalid user id");
            obj = new c.b(new Exception("Invalid user id"));
        } else {
            try {
                char[] cArr = b.b.a.c.f1097a;
                MessageDigest instance = MessageDigest.getInstance("SHA-256");
                instance.update((")(*&^%$#" + str2).getBytes());
                if (Arrays.equals(instance.digest(), loginDataSource.f1391c)) { // Usage of earlier string, password check
                    Log.d("ctflevel2", "Valid credentials entered");
                    try {
                        String str3 = str + ":" + str2;
                        char[] cArr2 = b.b.a.c.f1097a;
                        MessageDigest instance2 = MessageDigest.getInstance("SHA-256");
                        instance2.update(str3.getBytes());
                        byte[] digest = instance2.digest();
                        Log.d("ctflevel2", "CONGRATS! The 1st flag is " + loginDataSource.a(digest));
                        Log.d("ctflevel2", "There is another flag. Good luck!");
                        // [truncated]
                    }
                    // [truncated]
                }
                // [truncated]
            }
            // [truncated]
        }
        // [truncated]
    }
}
```

To find username, we check source code of `a(loginDataSource).toString()`

```java
// b.b.a.d
public class a {
    public String toString() {
        // [truncated]
        return new String(new byte[]{(byte) (-1462734071 >>> 4), (byte) (-385552254 >>> 9), (byte) (1107918732 >>> 19), (byte) (-198649565 >>> 6), (byte) (728446419 >>> 19), (byte) (718529411 >>> 17), (byte) (-2089595746 >>> 19)});
    }
}
```

Compile this in a local java file and print string to find the username.

```java
class GetUsername {  
  public static void main(String args[]) { 
    String x = new String(new byte[]{(byte) (-1462734071 >>> 4), (byte) (-385552254 >>> 9), (byte) (1107918732 >>> 19), (byte) (-198649565 >>> 6), (byte) (728446419 >>> 19), (byte) (718529411 >>> 17), (byte) (-2089595746 >>> 19)});
    System.out.println(x); 
  } 
}
// 0xAdmin
```

In the password check, the password is salted with prefix `")(*&^%$#"` and then checked against hash in `LoginDataSource`. Try a dictionary attack.

```python
from hashlib import sha256

target = "516b36ed915a70852daf6a06c7fd1a1451d8269a8b2c5ae97110bc77b083c420"
prefix = ")(*&^%$#"

# Wordlist from https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
with open('rockyou.txt', 'r') as f:
    line = f.readline()

    while line:
        passwd = line.strip()
        m = sha256()
        m.update((prefix + passwd).encode('utf-8'))
        if m.hexdigest() == target:
            print(f'!!! {prefix + passwd}')
            break

        line = f.readline()
# !!! )(*&^%$#aeroplane
```

Username is `0xAdmin`, password is `aeroplane`.

Flag is `DSO-NUS{34f37b328d0e1666dcf86307dc1bdbbdb3605750385650069ac74ac1edeb359f}`.