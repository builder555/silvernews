FROM mcr.microsoft.com/dotnet/sdk:8.0 as builder

WORKDIR /app

COPY . .

RUN dotnet build

EXPOSE 5122

CMD dotnet run
