# https://hub.docker.com/_/microsoft-dotnet
#
# BUILD stage
#
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build

# copy common, application files
WORKDIR /
COPY ./Common/ /Common/
COPY ./CongressMemberAPI/ /CongressMemberAPI/

# build app
WORKDIR /CongressMemberAPI
RUN dotnet publish -c release -o /Release

#
# RUN stage
#
FROM mcr.microsoft.com/dotnet/aspnet:7.0
WORKDIR /CongressMemberAPI
COPY --from=build /Release ./
ENTRYPOINT ["dotnet", "CongressMemberAPI.dll"]