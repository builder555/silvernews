namespace service_auth.Models;

public class JwtOptions
{
    public string JwtKey { get; set; }
    public string JwtIssuer { get; set; }
    public int JwtExpireMinutes { get; set; }
}