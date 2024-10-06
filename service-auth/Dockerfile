FROM mcr.microsoft.com/dotnet/sdk:8.0 as builder

WORKDIR /app

# Copy csproj and restore as distinct layers
COPY ./service-auth.csproj ./service-auth.csproj

RUN dotnet restore


# Copy everything else and build
COPY . ./
ENV ASPNETCORE_Environment=Docker
#RUN dotnet publish -c Debug -o out ./service-auth.csproj
RUN dotnet publish -c Release -o out ./service-auth.csproj


# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=builder /app/out .

EXPOSE 5122
EXPOSE 8080

CMD dotnet service-auth.dll
