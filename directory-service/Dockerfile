FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /app
COPY app /app
RUN dotnet publish -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:5.0
WORKDIR /app
COPY --from=build /app/publish /app


# install debugging tools
RUN apt update && apt install -y procps curl dnsutils

EXPOSE 80


CMD dotnet DirectoryService.dll
