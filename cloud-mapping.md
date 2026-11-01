# CloudNotes Compute Engine mapping

| Local deployment | Compute Engine equivalent | Why they play the same role |
|---|---|---|
| Linux server (VirtualBox / UTM / WSL / Docker) | Compute Engine VM (`e2-medium`, Ubuntu) | Both provide the Linux runtime where CloudNotes and its service manager execute. |
| Terminal / shell | `gcloud compute ssh` | Both provide an interactive way to administer the server. |
| `localhost:5000` / VM IP | VM static external IP | Both are the network address clients use to reach the application. |
| OS firewall / open port | GCP VPC firewall rule (`tcp:5000`) | Both permit inbound TCP traffic to the application port. |
| systemd | systemd on the VM | Both start CloudNotes at boot and restart it after a crash. |
| PostgreSQL on the environment | Cloud SQL (managed, LU 2.7) | Both provide the PostgreSQL database that stores notes independently of the app process. |
| `.env` / environment variables | Instance metadata / Secret Manager | Both supply runtime configuration without hard-coding secrets in source. |

The local request path is browser -> host or VM network -> firewall/open port ->
Linux server -> Flask bound to `0.0.0.0:5000`. In Compute Engine, the VM's
static external IP and VPC firewall rule replace the local host/VM networking
and OS-port-opening step.
