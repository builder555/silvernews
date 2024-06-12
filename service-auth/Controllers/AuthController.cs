
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using service_auth.Models;

namespace service_auth.Controllers;

public class AuthController : Controller
{
    public JwtOptions? JwtOptions { get; }

    public AuthController(IOptions<JwtOptions> jwtOptions)
    {
        JwtOptions = jwtOptions?.Value;
    }

    [HttpGet("api/[controller]/[action]")]
    [Authorize]
    public IActionResult Check()
    {
        return Ok();
    }

    [HttpGet("api/[controller]/[action]")]
    [Authorize(Roles = "Admin")]
    public IActionResult Admin()
    {
        return Json(true);
    }

    [HttpGet("api/[controller]/[action]")]
    [Authorize]
    public string GetToken()
    {
        var userId = this.User.FindFirstValue(ClaimTypes.NameIdentifier);

        var claims = new List<Claim>
            {
                new Claim(JwtRegisteredClaimNames.Sub, this.User.FindFirst(ClaimTypes.Name)?.Value),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
                new Claim(ClaimTypes.NameIdentifier, userId),
            };

        var givenName = this.User.FindFirstValue(ClaimTypes.GivenName);
        if (!string.IsNullOrEmpty(givenName))
        {
            claims.Add(new Claim(ClaimTypes.GivenName, givenName));
        }

        var roles = this.User.Claims.Where(c => c.Type == ClaimTypes.Role).Select(r => r.Value).ToList();

        if (roles != null && roles.Count() > 0)
        {
            claims.Add(new Claim("rls", string.Join(',', roles)));
        }

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(JwtOptions.JwtKey));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
        var expires = DateTime.Now.AddMinutes(JwtOptions.JwtExpireMinutes);

        var token = new JwtSecurityToken(
            JwtOptions.JwtIssuer,
            JwtOptions.JwtIssuer,
            claims,
            expires: expires,
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}