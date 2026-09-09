"""
MJ Tech Hub - Batch 2 Cloud & AI Tutorials Content
Tutorials:
1. aws-ec2-instance-families-and-purchasing-models
2. aws-vpc-architecture-subnets-route-tables-and-internet-gateways
3. cloud-iam-policy-syntax-json-statements-and-least-privilege
"""

CLOUD_TUTORIALS = [
    {
        "id": "aws-ec2-instance-families-and-purchasing-models",
        "title": "Amazon EC2 Architecture: Instance Types & Purchasing Options",
        "category": "Cloud & AI",
        "category_dir": "cloud",
        "category_page": "cloud.html",
        "level": "Intermediate",
        "readTime": "9 min read",
        "description": "Architect cloud compute on Amazon EC2: instance families (General Purpose, Compute, Memory, Storage), hardware virtualization (Nitro), and modern purchasing options (Savings Plans, Spot, On-Demand).",
        "keywords": "aws, ec2, instance types, purchasing options, savings plans, spot instances, on-demand, reserved instances, nitro system, cloud computing",
        "html": r"""<p><strong>Amazon Elastic Compute Cloud (Amazon EC2)</strong> is the core Infrastructure-as-a-Service (IaaS) compute service offered by Amazon Web Services (AWS). Provisioning virtual servers in the cloud requires infrastructure architects to navigate two critical architectural decisions: selecting the optimal <strong>Instance Type & Family</strong> tailored to application CPU/memory ratios, and choosing the cost-effective <strong>Billing & Purchasing Option</strong> to avoid cloud financial waste (FinOps).</p>

<h2>The AWS Nitro System: The Hypervisor Revolution</h2>
<p>Modern EC2 instance generations (generations 5, 6, and 7+) run on the <strong>AWS Nitro System</strong>. In legacy cloud virtualization, the host CPU spent significant processing cycles managing software hypervisor tasks: virtualizing network packets, managing EBS storage I/O, and tracking hardware interrupts.</p>
<p>The Nitro architecture offloads these hypervisor operations onto dedicated, custom-built Nitro ASIC PCIe cards:</p>
<ul>
    <li><strong>Nitro Card for VPC:</strong> Hardware-accelerated Enhanced Networking providing up to 100+ Gbps throughput with low latency and jitter.</li>
    <li><strong>Nitro Card for EBS:</strong> Dedicated NVMe controller handling Amazon Elastic Block Store volume encryption and I/O offload.</li>
    <li><strong>Nitro Security Chip:</strong> Provides a hardware Root of Trust that continuously validates firmware and locks down physical hardware access.</li>
    <li><strong>Result:</strong> Nearly 100% of host CPU and memory resources are dedicated to the customer's guest virtual machine, eliminating "noisy neighbor" contention.</li>
</ul>

<h2>Amazon EC2 Instance Families & Naming Conventions</h2>
<p>AWS organizes hundreds of compute instance types into standardized instance families. The alphanumeric naming convention indicates hardware characteristics:</p>

<div class="callout callout-info">
    <div class="callout-title"><i class="fa-solid fa-microchip" aria-hidden="true"></i> Decoding the Instance Name: <code>m6i.2xlarge</code></div>
    <div class="callout-body">
        <ul>
            <li><code>m</code>: <strong>Instance Family</strong> (General Purpose).</li>
            <li><code>6</code>: <strong>Generation</strong> (6th generation hardware).</li>
            <li><code>i</code>: <strong>Processor Architecture</strong> (<code>i</code> = Intel Xeon, <code>a</code> = AMD EPYC, <code>g</code> = AWS Graviton ARM).</li>
            <li><code>2xlarge</code>: <strong>Instance Size</strong> (dictates vCPU, RAM, network bandwidth, and EBS throughput).</li>
        </ul>
    </div>
</div>

<h3>Primary Enterprise Instance Families</h3>
<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Family Category</th>
                <th>Prefixes</th>
                <th>vCPU to RAM Ratio</th>
                <th>Target Enterprise Workloads</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>General Purpose</strong></td>
                <td><code>m6i</code>, <code>m7g</code>, <code>t4g</code></td>
                <td>1 vCPU : 4 GiB RAM</td>
                <td>Web and application servers, microservices, enterprise build test environments</td>
            </tr>
            <tr>
                <td><strong>Compute Optimized</strong></td>
                <td><code>c6i</code>, <code>c7g</code></td>
                <td>1 vCPU : 2 GiB RAM</td>
                <td>High-performance web servers, scientific modeling, batch processing, video encoding</td>
            </tr>
            <tr>
                <td><strong>Memory Optimized</strong></td>
                <td><code>r6i</code>, <code>r7g</code>, <code>x2iedn</code></td>
                <td>1 vCPU : 8 GiB (or higher)</td>
                <td>High-performance relational databases (MySQL, Oracle), in-memory caches (Redis, SAP HANA)</td>
            </tr>
            <tr>
                <td><strong>Storage Optimized</strong></td>
                <td><code>i3en</code>, <code>i4i</code></td>
                <td>Attached NVMe SSDs</td>
                <td>NoSQL distributed databases (Cassandra, MongoDB), distributed file systems, Elasticsearch</td>
            </tr>
            <tr>
                <td><strong>Accelerated / GPU</strong></td>
                <td><code>g5</code>, <code>p4de</code>, <code>p5</code></td>
                <td>NVIDIA Tensor GPUs</td>
                <td>Machine Learning training/inference, LLMs, 3D rendering, autonomous vehicle simulations</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Modern EC2 Billing & Purchasing Options</h2>
<p>Selecting the incorrect purchasing model can inflate cloud bills by 300% to 500%. AWS offers multiple billing commitments designed for different operational profiles:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Purchasing Option</th>
                <th>Pricing Model & Commitment</th>
                <th>Typical Cost Discount</th>
                <th>Ideal Operational Use Case</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>On-Demand</strong></td>
                <td>Pay-per-second, zero upfront commitment</td>
                <td>Baseline (0%)</td>
                <td>Short-term, spiky, unpredictable workloads or dev testing under 3 months</td>
            </tr>
            <tr>
                <td><strong>Compute Savings Plans</strong></td>
                <td>1-year or 3-year hourly spend commitment ($/hr)</td>
                <td>Up to 66% discount</td>
                <td>Dynamic containerized fleets; applies across EC2, AWS Fargate, and AWS Lambda</td>
            </tr>
            <tr>
                <td><strong>EC2 Instance Savings Plans</strong></td>
                <td>1-year or 3-year commitment to an individual instance family in a region</td>
                <td>Up to 72% discount</td>
                <td>Stable, long-term production database and application clusters with known sizing</td>
            </tr>
            <tr>
                <td><strong>Spot Instances</strong></td>
                <td>Bid on unused excess AWS compute capacity</td>
                <td>Up to 90% discount</td>
                <td>Fault-tolerant, interruptible workloads: batch data processing, CI/CD runners, rendering</td>
            </tr>
            <tr>
                <td><strong>Dedicated Hosts</strong></td>
                <td>Physical server fully dedicated to your organization</td>
                <td>High cost / Per-host billing</td>
                <td>Strict regulatory compliance, BYOL software licensing (per-socket/per-core licenses)</td>
            </tr>
        </tbody>
    </table>
</div>

<h3>Savings Plans vs Legacy Reserved Instances (RIs)</h3>
<p>While AWS still supports legacy Reserved Instances, <strong>AWS Savings Plans</strong> represent modern enterprise FinOps standard practice. Unlike standard RIs (which tied organizations to an exact operating system and instance size), Compute Savings Plans automatically apply discounts regardless of instance family, size, OS, availability zone, or even whether the workload migrates from EC2 to Fargate serverless containers.</p>

<h3>The Spot Instance 2-Minute Interruption Rule</h3>
<div class="callout callout-warning">
    <div class="callout-title"><i class="fa-solid fa-clock" aria-hidden="true"></i> Operating with Spot Interruptions</div>
    <div class="callout-body">AWS can reclaim Spot Instances whenever capacity is needed by On-Demand customers. AWS emits an Amazon EventBridge event and an EC2 Instance Metadata Service warning exactly <strong>two minutes prior to instance termination</strong>. Spot workloads must be completely stateless and architected with automated graceful shutdown hooks.</div>
</div>

<h2>Summary</h2>
<p>Mastering Amazon EC2 requires aligning workload performance requirements with hardware architecture and leveraging modern purchasing models. By deploying Graviton-powered ARM instances for superior price-performance, pairing steady-state production nodes with Savings Plans, and bursting batch workloads onto Spot Instances, cloud architects achieve maximum scalability with rigorous cost optimization.</p>"""
    },
    {
        "id": "aws-vpc-architecture-subnets-route-tables-and-internet-gateways",
        "title": "Amazon VPC Architecture: Public/Private Subnets, Route Tables & Internet Gateways",
        "category": "Cloud & AI",
        "category_dir": "cloud",
        "category_page": "cloud.html",
        "level": "Intermediate",
        "readTime": "9 min read",
        "description": "Architect resilient enterprise cloud networks: Amazon Virtual Private Cloud (VPC) CIDR design, multi-AZ public and private subnets, Route Tables, Internet Gateways, and NAT Gateways.",
        "keywords": "aws, vpc, subnet, route table, internet gateway, nat gateway, cidr, cloud networking, security group, nacl",
        "html": r"""<p>A secure enterprise cloud deployment begins with network isolation. In Amazon Web Services, the <strong>Amazon Virtual Private Cloud (Amazon VPC)</strong> is the foundational software-defined network (SDN) boundary that provisions a private, isolated virtual network topology. Understanding how subnets, route tables, Internet Gateways (IGW), and NAT Gateways interact is mandatory for securing cloud applications against unauthorized public internet exposure.</p>

<h2>VPC CIDR Architecture & Multi-AZ Subnet Planning</h2>
<p>When provisioning a VPC, the architect assigns a primary IPv4 Classless Inter-Domain Routing (CIDR) block (typically an RFC 1918 private range between <code>/16</code> and <code>/28</code>, such as <code>10.0.0.0/16</code> providing 65,536 private IP addresses).</p>

<div class="callout callout-warning">
    <div class="callout-title"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i> The 5 Reserved IPs in Every AWS Subnet</div>
    <div class="callout-body">
        In standard networking, an IPv4 subnet loses 2 addresses (network address and broadcast address). <strong>In AWS, every subnet reserves 5 IP addresses</strong> that cannot be assigned to customer resources:<br>
        1. <code>10.0.1.0</code>: Network address.<br>
        2. <code>10.0.1.1</code>: Reserved by AWS for the VPC default router.<br>
        3. <code>10.0.1.2</code>: Reserved by AWS for the internal Amazon DNS (AmazonProvidedDNS).<br>
        4. <code>10.0.1.3</code>: Reserved by AWS for future operational use.<br>
        5. <code>10.0.1.255</code>: Network broadcast address (broadcast is not supported in VPC).<br>
        A <code>/24</code> subnet therefore yields <strong>251 usable IP addresses</strong>, not 254.
    </div>
</div>

<h2>The Multi-Tier Subnet Topology</h2>
<p>Enterprise cloud architectures never deploy application servers or databases directly to public-facing networks. Modern VPCs utilize a multi-tier, multi-Availability Zone (AZ) layout:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Subnet Tier</th>
                <th>Subnet Routing Destination</th>
                <th>Public IP Assignment?</th>
                <th>Hosted Workloads</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Public Subnet</strong></td>
                <td>Route <code>0.0.0.0/0</code> pointed directly to Internet Gateway (<code>igw-xxxx</code>)</td>
                <td>Yes (Public IPv4 / Elastic IPs)</td>
                <td>Public Application Load Balancers (ALB), Bastion Hosts / NAT Gateways</td>
            </tr>
            <tr>
                <td><strong>Private App Subnet</strong></td>
                <td>Route <code>0.0.0.0/0</code> pointed to a NAT Gateway (<code>nat-xxxx</code>)</td>
                <td>No (Private RFC 1918 IPs only)</td>
                <td>Web servers, backend API microservices, container clusters (ECS/EKS)</td>
            </tr>
            <tr>
                <td><strong>Isolated DB Subnet</strong></td>
                <td>Local VPC route only (zero route to IGW or NAT)</td>
                <td>No</td>
                <td>Relational databases (Amazon RDS, Aurora), Redis/Memcached clusters</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Internet Gateways (IGW) vs NAT Gateways</h2>
<p>Managing outbound and inbound connectivity requires pairing the correct gateway component with subnet Route Tables:</p>

<h3>1. Internet Gateway (IGW)</h3>
<ul>
    <li>A horizontally scaled, redundant, highly available VPC component that imposes zero availability risks or bandwidth bottlenecks.</li>
    <li>Performs 1-to-1 Network Address Translation (NAT) between public IPv4 addresses and private instances.</li>
    <li>A subnet is defined as "public" <em>if and only if</em> its associated Route Table contains an explicit default route pointing to an attached Internet Gateway: <code>0.0.0.0/0 -> igw-xxxx</code>.</li>
</ul>

<h3>2. NAT Gateway</h3>
<ul>
    <li>Enables instances residing in private subnets to initiate outbound connections to the internet (for software package updates, OS patches, or third-party API calls) while <strong>preventing external internet clients from initiating inbound connections</strong> to those instances.</li>
    <li>Deployed inside a <strong>public subnet</strong> and allocated a dedicated Elastic IP address.</li>
    <li>Private subnet Route Tables direct their outbound default traffic to the NAT Gateway: <code>0.0.0.0/0 -> nat-xxxx</code>.</li>
</ul>

<div class="callout callout-info">
    <div class="callout-title"><i class="fa-solid fa-cloud" aria-hidden="true"></i> High Availability Design: One NAT Gateway Per AZ</div>
    <div class="callout-body">A NAT Gateway is an Availability Zone-specific resource. If Availability Zone 1 fails, instances in AZ 2 relying on AZ 1's NAT Gateway lose outbound connectivity. In production, deploy one NAT Gateway in each AZ to maintain multi-AZ fault isolation.</div>
</div>

<h2>Security Groups vs Network Access Control Lists (NACLs)</h2>
<p>AWS enforces traffic filtering using two distinct firewall layers within the VPC:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Security Attribute</th>
                <th>Security Groups</th>
                <th>Network Access Control Lists (NACLs)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Level of Operation</strong></td>
                <td>Instance / Elastic Network Interface (ENI) level</td>
                <td>Subnet boundary level</td>
            </tr>
            <tr>
                <td><strong>Statefulness</strong></td>
                <td><strong>Stateful:</strong> Return traffic is automatically permitted regardless of inbound rules</td>
                <td><strong>Stateless:</strong> Return traffic must be explicitly allowed via outbound ephemeral port rules</td>
            </tr>
            <tr>
                <td><strong>Rule Evaluation</strong></td>
                <td>All rules evaluated before deciding to permit traffic</td>
                <td>Rules processed in strict numerical order (lowest number evaluated first)</td>
            </tr>
            <tr>
                <td><strong>Deny Rules</strong></td>
                <td>Only supports Allow rules (implicit deny all)</td>
                <td>Supports explicit Allow and explicit Deny rules</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Cross-Cloud Analogy: AWS VPC vs Microsoft Azure VNet</h2>
<p>Engineers operating in multi-cloud environments map these constructs directly to Microsoft Azure:</p>
<ul>
    <li>An <strong>AWS VPC</strong> equates to an <strong>Azure Virtual Network (VNet)</strong>.</li>
    <li>An <strong>AWS Internet Gateway / Route Table</strong> maps to <strong>Azure User-Defined Routes (UDR)</strong> and Azure Virtual Network Gateways.</li>
    <li>An <strong>AWS Security Group</strong> maps directly to an <strong>Azure Network Security Group (NSG)</strong>.</li>
</ul>

<h2>Summary</h2>
<p>Designing an enterprise Amazon VPC demands a disciplined separation of public and private tiers. By provisioning multi-AZ subnets, deploying NAT Gateways for secure outbound egress, and isolating sensitive databases into completely air-gapped private subnets, cloud engineers construct scalable and fortified cloud network architectures.</p>"""
    },
    {
        "id": "cloud-iam-policy-syntax-json-statements-and-least-privilege",
        "title": "AWS IAM JSON Policies: Statements & Principle of Least Privilege",
        "category": "Cloud & AI",
        "category_dir": "cloud",
        "category_page": "cloud.html",
        "level": "Intermediate",
        "readTime": "8 min read",
        "description": "Master AWS Identity and Access Management (IAM) JSON policy architecture: Effect, Action, Resource, and Condition blocks, evaluation logic, and least privilege enforcement.",
        "keywords": "aws, iam, json policy, least privilege, polp, statement, effect, action, resource, condition, cloud security",
        "html": r"""<p>In Amazon Web Services (AWS), authorization is governed universally by <strong>AWS Identity and Access Management (IAM) Policy Documents</strong>. Whether an API call is made by a software developer clicking the AWS Management Console, an automated Terraform pipeline running in CI/CD, or an Amazon EC2 instance querying an Amazon S3 bucket, AWS evaluates an attached JSON policy document to permit or deny the request.</p>
<p>Authoring secure, auditable IAM policies is the primary defense against catastrophic cloud data breaches and privilege escalation.</p>

<h2>The Anatomy of an AWS IAM JSON Policy Document</h2>
<p>An IAM policy is an explicit JSON object containing a top-level <code>Version</code> and an array of one or more <code>Statement</code> objects:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-file-code" aria-hidden="true"></i> Secure S3 Read-Only Policy Example</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code>{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSpecificS3BucketRead",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::corp-financial-reports-2026",
                "arn:aws:s3:::corp-financial-reports-2026/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "true"
                }
            }
        }
    ]
}</code></pre>
</div>

<h2>Deconstructing Policy Statement Elements</h2>
<ul>
    <li><strong><code>Version</code>:</strong> Defines the language syntax rules. Always declare <code>"2012-10-17"</code>. (Never omit this or use the current calendar date, as legacy versions fail to process modern policy variables).</li>
    <li><strong><code>Sid</code> (Statement ID):</strong> An optional, human-readable identifier describing the business intent of the statement.</li>
    <li><strong><code>Effect</code>:</strong> Explicitly states whether the policy grants or denies access. Accepts only two values: <code>"Allow"</code> or <code>"Deny"</code>.</li>
    <li><strong><code>Action</code>:</strong> The specific AWS service API calls being controlled. Expressed as <code>service:operation</code> (e.g. <code>ec2:StartInstances</code>, <code>dynamodb:Query</code>). Wildcards (<code>*</code>) are supported but should be strictly curtailed in production.</li>
    <li><strong><code>Resource</code>:</strong> The Amazon Resource Name (ARN) identifying the exact AWS object to which the action applies. Notice in the S3 example that bucket operations (<code>ListBucket</code>) require the bucket ARN (<code>arn:aws:s3:::bucket</code>), while object operations (<code>GetObject</code>) require the wildcard object ARN (<code>arn:aws:s3:::bucket/*</code>).</li>
    <li><strong><code>Condition</code>:</strong> The most powerful authorization block, evaluating environmental context (e.g. source IP, TLS cipher, MFA status, current timestamp, or resource tags).</li>
</ul>

<h2>The AWS Policy Evaluation Logic: The Explicit Deny Rule</h2>
<p>When an API call is executed, the AWS IAM evaluation engine follows a deterministic, non-negotiable decision tree:</p>

<div class="table-responsive">
    <table>
        <thead>
            <tr>
                <th>Evaluation Step</th>
                <th>Evaluation Logic</th>
                <th>Result</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Default State</strong></td>
                <td>By default, all requests are implicitly denied</td>
                <td>Implicit Deny</td>
            </tr>
            <tr>
                <td><strong>2. Explicit Deny Check</strong></td>
                <td>Does ANY applicable policy contain <code>"Effect": "Deny"</code> matching this Action and Resource?</td>
                <td><strong>Immediate Deny.</strong> Evaluation halts immediately. An explicit deny overrides all allows.</td>
            </tr>
            <tr>
                <td><strong>3. Explicit Allow Check</strong></td>
                <td>Does at least ONE applicable policy contain <code>"Effect": "Allow"</code>?</td>
                <td><strong>Request Permitted.</strong></td>
            </tr>
            <tr>
                <td><strong>4. Final Fallback</strong></td>
                <td>No explicit Allow found and no explicit Deny found</td>
                <td><strong>Implicit Deny.</strong> Request rejected.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="callout callout-warning">
    <div class="callout-title"><i class="fa-solid fa-shield-halved" aria-hidden="true"></i> The Absolute Power of Explicit Deny</div>
    <div class="callout-body">Even if a user belongs to the <code>AdministratorAccess</code> group granting <code>*:*</code> (Full Administrative Access), if a Service Control Policy (SCP) or boundary policy contains a statement with <code>"Effect": "Deny"</code> for <code>s3:DeleteBucket</code>, the user is permanently blocked from deleting S3 buckets.</div>
</div>

<h2>Operationalizing the Principle of Least Privilege (PoLP)</h2>
<p>The <strong>Principle of Least Privilege</strong> mandates that identities should be granted only the minimum permissions necessary to complete their specific business function—nothing more.</p>

<h3>Anti-Pattern: The Dangerous Wildcard Administrator</h3>
<p>Novice cloud practitioners frequently write overly broad policies to eliminate permission errors quickly:</p>
<pre><code>{
    "Effect": "Allow",
    "Action": "s3:*",
    "Resource": "*"
}</code></pre>
<p>If an application server running under this policy is compromised via an SSRF (Server-Side Request Forgery) flaw, the attacker can list, download, overwrite, and delete every S3 bucket across the entire AWS account.</p>

<h3>Best Practice: Granular Action & Resource Scoping with Conditions</h3>
<p>Enforce contextual constraints using <code>Condition</code> blocks:</p>

<div class="tutorial-command">
    <div class="command-header">
        <span class="command-label"><i class="fa-solid fa-file-code" aria-hidden="true"></i> Mandatory MFA & Corporate IP Restriction Policy</span>
        <button class="btn-copy-code" type="button" aria-label="Copy code snippet"><i class="fa-regular fa-copy" aria-hidden="true"></i> Copy</button>
    </div>
    <pre><code>{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyAllWithoutMFAAndCorporateIP",
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                },
                "NotIpAddressIfExists": {
                    "aws:SourceIp": [
                        "198.51.100.0/24",
                        "203.0.113.50/32"
                    ]
                }
            }
        }
    ]
}</code></pre>
</div>

<h2>Eliminating Long-Lived Access Keys: IAM Roles for Workloads</h2>
<p>Never hardcode static AWS Access Keys (<code>AKIA...</code>) inside application configuration files or EC2 servers. Modern cloud architecture mandates attaching an <strong>IAM Role</strong> directly to the compute resource via an Instance Profile. The instance queries the AWS Instance Metadata Service (IMDSv2) to obtain ephemeral, short-lived security tokens that automatically rotate every 6 hours.</p>

<h2>Summary</h2>
<p>AWS IAM JSON policies are the bedrock of cloud governance. By mastering the <code>Version</code>, <code>Statement</code>, <code>Effect</code>, <code>Action</code>, <code>Resource</code>, and <code>Condition</code> schema, respecting the non-negotiable priority of Explicit Deny, and applying the Principle of Least Privilege, cloud architects construct impenetrable cloud security perimeters.</p>"""
    }
]
