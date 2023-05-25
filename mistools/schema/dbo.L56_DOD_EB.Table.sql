USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_EB]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_EB]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_EB]
GO
/****** Object:  Table [dbo].[L56_DOD_EB]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_EB](
	[GI01] [varchar](3) NULL,
	[GI03] [varchar](3) NOT NULL,
	[EB00] [varchar](9) NOT NULL,
	[EB01] [varchar](1) NULL,
	[EB02] [varchar](8) NULL,
	[STD1] [decimal](5, 0) NULL,
	[EB03] [varchar](1) NULL,
	[EB05] [varchar](1) NULL,
	[EB06] [varchar](1) NULL,
	[EB07] [varchar](1) NULL,
	[EB08] [varchar](1) NULL,
	[EB09] [varchar](1) NULL,
	[EB11] [varchar](1) NULL,
	[EB12] [int] NULL,
	[EB13] [int] NULL,
	[EB14] [varchar](21) NULL,
	[EBD1] [varchar](1) NULL,
 CONSTRAINT [PK_DOD_EB_GI03_EB00] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[EB00] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
