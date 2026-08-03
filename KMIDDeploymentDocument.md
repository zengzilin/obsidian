# **Environment Pre-Requisites** 

1.  IIS

2.  .Net 8.0

3.  Domain SSL Certificate of Windows Server(if needed)

4.  KMID PACI Certificate

## Install IIS

1.  search "Server Manager"

<img
src="KMIDDeploymentDocument_media/media/image1.png"
style="width:6.29931in;height:6.26777in" alt="descript" />

2.  click "Manage" -\> "Add Roles and Features"

<img
src="KMIDDeploymentDocument_media/media/image2.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

3.  Follow installing step like below

<img
src="KMIDDeploymentDocument_media/media/image3.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image4.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image5.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image6.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image7.png"
style="width:4.33333in;height:4.33333in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image8.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image9.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image10.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image11.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image12.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

4.  Install Successfully

<img
src="KMIDDeploymentDocument_media/media/image13.png"
style="width:6.29931in;height:4.48805in" alt="descript" />

## Install .Net 8.0

1.  Open [Download .NET 8.0 (Linux, macOS, and Windows) \|
    .NET](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

2.  Download .Net 8.0

<img
src="KMIDDeploymentDocument_media/media/image14.png"
style="width:6.29931in;height:3.14735in" alt="descript" />

3.  Follow installing step like below

<img
src="KMIDDeploymentDocument_media/media/image15.png"
style="width:4.90625in;height:3.54167in" alt="descript" />

4.  Install Successfully

<img
src="KMIDDeploymentDocument_media/media/image16.png"
style="width:4.90625in;height:3.54167in" alt="descript" />

## Install Domain SSL Certificate(if needed)

## Install KMID PACI SSL Certificate

1.  Install Certificate to "Local Machine"(need provided by kmid first)

<img
src="KMIDDeploymentDocument_media/media/image17.png"
style="width:5.57292in;height:5.44792in" alt="descript" />

2.  Next step

<img
src="KMIDDeploymentDocument_media/media/image18.png"
style="width:5.57292in;height:5.44792in" alt="descript" />

3.  Input password

<img
src="KMIDDeploymentDocument_media/media/image19.png"
style="width:5.57292in;height:5.44792in" alt="descript" />

4.  Change certificate installation location

<img
src="KMIDDeploymentDocument_media/media/image20.png"
style="width:5.57292in;height:5.44792in" alt="descript" />

5.  Select "Personal"

<img
src="KMIDDeploymentDocument_media/media/image21.png"
style="width:2.92708in;height:2.73958in" alt="descript" />

6.  Install successfully

<img
src="KMIDDeploymentDocument_media/media/image22.png"
style="width:5.57292in;height:5.44792in" alt="descript" />

# **Deployment Flow**

1.  Open IIS

<img
src="KMIDDeploymentDocument_media/media/image23.png"
style="width:6.29931in;height:5.81105in" alt="descript" />

2.  Add website

<img
src="KMIDDeploymentDocument_media/media/image24.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

3.  Input website message

Site name: the name of website like MIDAuthWebService

Application pool: select or create a new application pool

Physical path: the deployment package path

Binding: if use https protol, that need to finished **1.3 Install Domain
SSL Certificate** first

Host name: the name of host like
[kwpreprodmobileid.tiqmopaymentkuwait.com](https://kwpreprodmobileid.tiqmopaymentkuwait.com)

SSL certificate: installed by **1.3 Install Domain SSL Certificate**

<img
src="KMIDDeploymentDocument_media/media/image25.png"
style="width:6.09375in;height:7in" alt="descript" />

4.  Make sure the website is associated with an application pool that
    you want

<img
src="KMIDDeploymentDocument_media/media/image26.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image27.png"
style="width:4.54167in;height:5.65625in" alt="descript" />

5.  Change the application pool ".Net CLR version" to "No Managed Code"

<img
src="KMIDDeploymentDocument_media/media/image28.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image29.png"
style="width:6.29931in;height:3.65186in" alt="descript" />

6.  Configure client SSL settings(if needed)

Default configuration is "ignore" which mean that client do not need to
provide the ssl certificate.If server want to verify the client
certificate, can check "Require SSL" option and then check "Require"
option, after that client need to provide the ssl certificate with each
api call.

<img
src="KMIDDeploymentDocument_media/media/image30.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

<img
src="KMIDDeploymentDocument_media/media/image31.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

# **Authorize Flow**

1.  Click "Browse Website"

<img
src="KMIDDeploymentDocument_media/media/image32.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

2.  HTTP Error 500.19 - Internal Server Error

it cases by website which does not have permission to read configuration

<img
src="KMIDDeploymentDocument_media/media/image33.png"
style="width:6.29931in;height:3.22898in" alt="descript" />

3.  Edit Permission

<img
src="KMIDDeploymentDocument_media/media/image34.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

4.  "Security" -\> "Edit"

<img
src="KMIDDeploymentDocument_media/media/image35.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

5.  "Add"

<img
src="KMIDDeploymentDocument_media/media/image36.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

6.  "Advanced"

<img
src="KMIDDeploymentDocument_media/media/image37.png"
style="width:6.29931in;height:3.19015in" alt="descript" />

7.  "Find Now"

Select IIS_IUSRS group(created by IIS automatically), also you could
select another or create a new group which satisfied with server running
requirement.

<img
src="KMIDDeploymentDocument_media/media/image38.png"
style="width:5.36458in;height:6.03125in" alt="descript" />

8.  Click "OK"

<img
src="KMIDDeploymentDocument_media/media/image39.png"
style="width:4.76042in;height:2.61458in" alt="descript" />

9.  Check "Modify" option

<img
src="KMIDDeploymentDocument_media/media/image40.png"
style="width:3.78125in;height:4.6875in" alt="descript" />

10. Add Group Successfully

<img
src="KMIDDeploymentDocument_media/media/image41.png"
style="width:3.78125in;height:5.01042in" alt="descript" />

11. Refresh Website

After above flow, refresh website could see the error page is
disappeared. The 404 error page is normal dut to the server do not have
any page.

<img
src="KMIDDeploymentDocument_media/media/image42.png"
style="width:6.29931in;height:2.84924in" alt="descript" />

you could visit: website + /swagger/index.html, can view the swagger
ui(will remove in production environment)

<img
src="KMIDDeploymentDocument_media/media/image43.png"
style="width:6.29931in;height:2.9946in" alt="descript" />

# **Environment Configuration**

1.  Windows Firewall Policy

2.  ...

# **Checklist**

1.  Domain Network Connectivity

2.  Domain Port Connectivity

3.  Service Availability
