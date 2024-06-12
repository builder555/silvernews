using Microsoft.AspNetCore.DataProtection;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using service_auth.Data;
using service_auth.Models;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));

var postgresConnection = builder.Configuration.GetConnectionString("Postgres") ?? throw new InvalidOperationException("Connection string 'Postgres' not found.");
builder.Services.AddDbContext<ApplicationDbContext>(options => {
    options.UseNpgsql(postgresConnection);
});

builder.Services.AddDbContext<DataProtectionContext>(options => {
    options.UseNpgsql(postgresConnection);
});

builder.Services.AddDataProtection().PersistKeysToDbContext<DataProtectionContext>();

builder.Services.AddDatabaseDeveloperPageExceptionFilter();

builder.Services.AddDefaultIdentity<IdentityUser>(options => options.SignIn.RequireConfirmedAccount = true)
    .AddEntityFrameworkStores<ApplicationDbContext>();
builder.Services.AddControllersWithViews();

var app = builder.Build();

using (var scope = app.Services.CreateScope()) {
    scope.ServiceProvider.GetRequiredService<ApplicationDbContext>().Database.Migrate();
    scope.ServiceProvider.GetRequiredService<DataProtectionContext>().Database.Migrate();
}

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseMigrationsEndPoint();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
app.MapRazorPages();

app.Run();
