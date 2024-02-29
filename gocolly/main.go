package main

import (
	"context"
	"fmt"
	"log"
	"github.com/chromedp/chromedp"
	"time"
)

func main() {
	// Create a new context for ChromeDP
	ctx, cancel := chromedp.NewContext(context.Background())
	defer cancel()
	// Define a variable to hold the HTML content
	var htmlContent string
	// Define the task to navigate to the login page, fill in the login form, and print the HTML content
	var getHTMLTask chromedp.Tasks = chromedp.Tasks{
		chromedp.Navigate(`http://10.15.0.51/cgi-bin/login.htm?logout=1`), // Adjust the URL as necessary
		chromedp.Evaluate(`document.querySelector("#username").value = "";`, nil),
		chromedp.WaitVisible(`#username`, chromedp.ByID),
		chromedp.SendKeys(`#username`, "admin", chromedp.ByID),
		chromedp.WaitVisible(`#password`, chromedp.ByID),
		chromedp.SendKeys(`#password`, "xxxx", chromedp.ByID),
		chromedp.Evaluate(`doLogin()`, nil), // Trigger the doLogin function
		chromedp.ActionFunc(func(ctx context.Context) error {
		    // Custom action to wait for the element with ID "UE_table" to exist
		    for {
		        // Check if the element with ID "UE_table" is visible
		        exists := false
		        err := chromedp.Evaluate(`document.querySelector("#ftr.lockedTr") !== null`, &exists).Do(ctx)
		        if err != nil {
		            return err
		        }
		        if exists {
		            fmt.Println("UE_table element exists")
		            break
		        }
		        // Wait for a short period before checking again
		        time.Sleep(50 * time.Millisecond)
		    }
		    return nil
		}),
		chromedp.InnerHTML("html", &htmlContent),
	}

	// Run the task
	if err := chromedp.Run(ctx, getHTMLTask); err != nil {
		log.Fatal(err)
	}

	// Print the HTML content
	fmt.Println(htmlContent)
}