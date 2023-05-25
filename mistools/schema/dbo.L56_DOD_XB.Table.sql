USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_XB]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_XB]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_XB]
GO
/****** Object:  Table [dbo].[L56_DOD_XB]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_XB](
	[GI01] [varchar](3) NULL,
	[GI03] [varchar](3) NOT NULL,
	[CB01] [varchar](12) NOT NULL,
	[XB00] [varchar](6) NOT NULL,
	[CB00] [varchar](12) NOT NULL,
	[XB01] [varchar](1) NULL,
	[XB02] [varchar](8) NULL,
	[XB04] [varchar](1) NULL,
	[XB05] [decimal](4, 2) NULL,
	[XB06] [decimal](4, 2) NULL,
	[XB07] [varchar](1) NULL,
	[XB08] [varchar](1) NULL,
	[XB09] [varchar](1) NULL,
	[XB10] [varchar](1) NULL,
	[XB11] [decimal](6, 2) NULL,
	[XBD1] [int] NULL,
	[XBD3] [varchar](1) NULL,
	[XBD4] [decimal](7, 1) NULL,
	[XBD5] [varchar](1) NULL,
	[XB12] [varchar](1) NULL,
 CONSTRAINT [PK_DOD_XB_GI03_CB00_XB00] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CB00] ASC,
	[XB00] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
