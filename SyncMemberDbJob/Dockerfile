# https://hub.docker.com/_/microsoft-dotnet
#
# BUILD stage
#
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build

# copy common, application files
WORKDIR /
COPY ./Common/ /Common/
COPY ./SyncMemberDbJob/ /SyncMemberDbJob/

# build app
WORKDIR /SyncMemberDbJob
RUN dotnet publish -c release -o /Release

#
# RUN stage
#
FROM mcr.microsoft.com/dotnet/aspnet:7.0
WORKDIR /SyncMemberDbJob
COPY --from=build /Release ./
ENTRYPOINT ["dotnet", "SyncMemberDbJob.dll"]